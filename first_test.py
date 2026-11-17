from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    print("页面标题是：", page.title())
    page.locator("#kw").fill("你好")
    page.locator("#su").click()
    print("搜索后的标题是：",page.title())
    assert_result_page(page, "你好")
 