# import time
#
# from playwright.sync_api import sync_playwright, Page
#
#
# def test_placeholder():
#     with sync_playwright() as p:
#         browser=p.chromium.launch(headless=False,args=["--start-maximized"])
#         context=browser.new_context(no_viewport=True)
#         page=context.new_page()
#
#         page.goto("https://devtr-anonymizationwebtool.sureprep.com/login")
#         page.get_by_text("Go to Anonymization Tool").click()
#         page.wait_for_selector("#username").fill("6124529")
#         page.locator("#password").fill("Scrambler@400T")
#         page.locator("#signOnButton").click()
#         page.wait_for_selector('[placeholder="Request ID..."]').fill("ABCD")
#         time.sleep(15)
#
#         time.sleep(5)
#
#
#
#

print("\n" + "="*80)