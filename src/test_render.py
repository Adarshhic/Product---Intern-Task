import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    base_dir = Path(__file__).resolve().parent.parent
    html_path = (base_dir / "web" / "index.html").resolve()
    screenshot_path = (base_dir / "web" / "screenshot.png").resolve()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(f"file:///{html_path.as_posix()}", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(screenshot_path), full_page=False)
        title = await page.title()
        table_rows = await page.locator("#matrixTableBody tr").count()
        print(f"Page Title: {title}")
        print(f"Rendered Table Rows: {table_rows}")
        print(f"Screenshot saved to: {screenshot_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
