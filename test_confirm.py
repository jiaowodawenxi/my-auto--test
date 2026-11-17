"""sahitest confirmTest.htm 页面的自动化测试用例。

页面核心元素：
- 按钮 "Click For Confirm"：点击后触发浏览器原生 confirm("Some question?")
- 文本框（form f1 中的 input t1）：显示 confirm 结果（"oked" / "canceled"）
- 链接 "Back"：返回上一页

运行前请安装依赖：
    pip install playwright pytest pytest-playwright
    playwright install chromium
"""

import pytest
from playwright.sync_api import expect

# 被测页面地址
TARGET_URL = "https://sahitest.com/demo/confirmTest.htm"


# ---------- 公共定位器 ----------

def btn_confirm(page):
    """定位 Click For Confirm 按钮。"""
    return page.get_by_role("button", name="Click For Confirm")


def input_result(page):
    """定位结果文本框 —— 页面上只有一个 textbox。"""
    return page.get_by_role("textbox")


def link_back(page):
    """定位 Back 链接。"""
    return page.get_by_role("link", name="Back")


# ---------- 测试用例 ----------


def test_page_loads_correctly(page):
    """TC01：页面正常加载 —— 核心元素均可见且可交互。"""
    page.goto(TARGET_URL)

    # 标题包含 Confirm Test
    expect(page.get_by_role("heading", name="Confirm Test")).to_be_visible()

    # 按钮、文本框、Back 链接都存在
    expect(btn_confirm(page)).to_be_visible()
    expect(input_result(page)).to_be_visible()
    expect(link_back(page)).to_be_visible()


def test_confirm_click_ok_sets_oked(page):
    """TC02：正常确定流程 —— 点击按钮后在 confirm 中点确定，文本框显示 oked。"""
    page.goto(TARGET_URL)

    # 监听 confirm 弹框，自动点确定
    page.on("dialog", lambda dialog: dialog.accept())

    btn_confirm(page).click()

    expect(input_result(page)).to_have_value("oked")


def test_confirm_click_cancel_sets_canceled(page):
    """TC03：正常取消流程 —— 点击按钮后在 confirm 中点取消，文本框显示 canceled。"""
    page.goto(TARGET_URL)

    # 监听 confirm 弹框，自动点取消
    page.on("dialog", lambda dialog: dialog.dismiss())

    btn_confirm(page).click()

    expect(input_result(page)).to_have_value("canceled")


def test_back_link_navigates(page):
    """TC04：返回流程 —— 点击 Back 链接后 URL 发生回退。"""
    page.goto(TARGET_URL)

    link_back(page).click()

    # Back 链接指向 sahitest demo 主页，URL 不再是 confirmTest.htm
    page.wait_for_load_state("domcontentloaded")
    assert "confirmTest.htm" not in page.url


def test_multiple_clicks_alternate_values(page):
    """TC05：连续点击按钮 —— 多次点击分别确定/取消，文本框正确更新。"""
    page.goto(TARGET_URL)

    # 第 1 次：确定 → oked
    page.once("dialog", lambda d: d.accept())
    btn_confirm(page).click()
    expect(input_result(page)).to_have_value("oked")

    # 第 2 次：取消 → canceled
    page.once("dialog", lambda d: d.dismiss())
    btn_confirm(page).click()
    expect(input_result(page)).to_have_value("canceled")

    # 第 3 次：确定 → oked
    page.once("dialog", lambda d: d.accept())
    btn_confirm(page).click()
    expect(input_result(page)).to_have_value("oked")


def test_initial_state_input_empty(page):
    """TC06：初始状态校验 —— 页面刚加载时文本框为空。"""
    page.goto(TARGET_URL)

    expect(input_result(page)).to_have_value("")


def test_esc_on_confirm_dismisses(page):
    """TC07：键盘 ESC 关闭 confirm —— ESC 等同于取消，文本框显示 canceled。"""
    page.goto(TARGET_URL)

    # Playwright 中 dismiss() 对应点击取消或按 ESC
    page.on("dialog", lambda dialog: dialog.dismiss())

    btn_confirm(page).click()

    expect(input_result(page)).to_have_value("canceled")


def test_enter_on_confirm_accepts(page):
    """TC08：键盘 Enter 确认 confirm —— Enter 等同于确定，文本框显示 oked。"""
    page.goto(TARGET_URL)

    # Playwright 中 accept() 对应点击确定或按 Enter
    page.on("dialog", lambda dialog: dialog.accept())

    btn_confirm(page).click()

    expect(input_result(page)).to_have_value("oked")
