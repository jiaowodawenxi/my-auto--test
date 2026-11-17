"""演示脚本：让 confirm 弹框停留 3 秒，肉眼看清后再点取消。

运行：python demo_confirm_cancel.py
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    # 步骤 1：打开页面
    print("[1/4] 打开页面...")
    page.goto("https://sahitest.com/demo/confirmTest.htm")
    page.wait_for_timeout(1500)

    # 步骤 2：设置 dialog 监听，弹框出现后等 3 秒再 dismiss（取消）
    print("[2/4] 点击按钮，confirm 弹框马上出现！停留 3 秒让你看清楚...")

    def handle_dialog(dialog):
        print(f"    ✅ 弹框来了！内容是: '{dialog.message}'")
        print("       3 秒后自动点【取消】...")
        page.wait_for_timeout(3000)   # 停 3 秒
        dialog.dismiss()               # 点取消

    page.on("dialog", handle_dialog)

    # 步骤 3：点击按钮触发弹框
    page.get_by_role("button", name="Click For Confirm").click()
    page.wait_for_timeout(1500)

    # 步骤 4：验证结果
    print("[3/4] 验证结果...")
    value = page.get_by_role("textbox").input_value()
    print(f"    文本框里显示: '{value}'")
    assert value == "canceled", f"预期 canceled, 实际 {value}"
    print("[4/4] ✅ 演示完成！5 秒后自动关闭浏览器...")
    page.wait_for_timeout(5000)

    browser.close()
