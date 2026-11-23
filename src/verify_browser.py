import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_PATH = (BASE_DIR / "index.html").as_uri()
SCREENSHOTS_DIR = BASE_DIR / "web" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

async def run_checks():
    console_messages = []
    page_errors = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Test 1280px (Desktop Dark)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        await page.goto(HTML_PATH)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "desktop_1280_dark.png"), full_page=False)

        # Toggle to Light mode
        await page.click("#themeToggleBtn")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "desktop_1280_light.png"), full_page=False)

        # Test Search Filter
        await page.fill("#searchInput", "Stripe")
        await page.wait_for_timeout(300)
        count_text = await page.text_content("#rowCount")
        print(f"Filter search 'Stripe' result text: {count_text}")
        await page.fill("#searchInput", "")
        await page.wait_for_timeout(300)

        # Test 768px (Tablet)
        await page.set_viewport_size({"width": 768, "height": 1024})
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "tablet_768_light.png"), full_page=False)

        # Toggle back to Dark mode
        await page.click("#themeToggleBtn")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "tablet_768_dark.png"), full_page=False)

        # Test 375px (Mobile)
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "mobile_375_dark.png"), full_page=False)

        # Check Horizontal Overflow on Mobile 375px
        scroll_width = await page.evaluate("() => document.documentElement.scrollWidth")
        client_width = await page.evaluate("() => document.documentElement.clientWidth")
        body_scroll = await page.evaluate("() => document.body.scrollWidth")
        print(f"Mobile 375px dimensions: scrollWidth={scroll_width}, clientWidth={client_width}, bodyScrollWidth={body_scroll}")

        await page.click("#themeToggleBtn")
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "mobile_375_light.png"), full_page=False)

        await browser.close()

    print(f"Console messages count: {len(console_messages)}")
    for m in console_messages:
        print(f"  {m}")
    print(f"Page errors count: {len(page_errors)}")
    for e in page_errors:
        print(f"  {e}")
    
    if scroll_width > client_width:
        print(f"WARNING: Horizontal overflow detected on 375px: {scroll_width} > {client_width}")
    else:
        print(f"SUCCESS: Zero horizontal overflow on 375px (scrollWidth={scroll_width} <= clientWidth={client_width})")

if __name__ == "__main__":
    asyncio.run(run_checks())
