"""
基礎 Page Object，包含所有頁面通用的操作方法。
使用 Playwright 內建等待機制 - 禁止使用 time.sleep！
"""
from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    """所有 Page Object 的基礎類別，提供通用操作。"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def goto(self, url: str, wait_until: str = "domcontentloaded") -> None:
        """導航至指定 URL。"""
        self.page.goto(url, wait_until=wait_until)
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """點擊元素。"""
        locator = self.page.locator(selector)
        if timeout:
            locator.click(timeout=timeout)
        else:
            locator.click()
    
    def fill(self, selector: str, value: str, clear_first: bool = True) -> None:
        """填寫輸入框。"""
        locator = self.page.locator(selector)
        if clear_first:
            locator.clear()
        locator.fill(value)
    
    def type_text(self, selector: str, value: str, delay: int = 50) -> None:
        """逐字輸入（適用於有驗證的輸入框）。"""
        locator = self.page.locator(selector)
        locator.press_sequentially(value, delay=delay)
    
    def wait_visible(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """等待元素可見。"""
        locator = self.page.locator(selector)
        try:
            count = locator.count()
        except Exception:
            count = 1
        if count > 1:
            for i in range(count):
                candidate = locator.nth(i)
                try:
                    if candidate.is_visible():
                        locator = candidate
                        break
                except Exception:
                    continue
        if timeout:
            expect(locator).to_be_visible(timeout=timeout)
        else:
            expect(locator).to_be_visible()
        return locator
    
    def wait_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        """等待元素隱藏。"""
        locator = self.page.locator(selector)
        if timeout:
            expect(locator).to_be_hidden(timeout=timeout)
        else:
            expect(locator).to_be_hidden()
    
    def assert_text(self, selector: str, expected_text: str, timeout: Optional[int] = None) -> None:
        """斷言元素包含指定文字。"""
        locator = self.page.locator(selector)
        if timeout:
            expect(locator).to_contain_text(expected_text, timeout=timeout)
        else:
            expect(locator).to_contain_text(expected_text)
    
    def assert_url_contains(self, url_part: str, timeout: Optional[int] = None) -> None:
        """斷言目前 URL 包含指定字串。"""
        if timeout:
            expect(self.page).to_have_url(f"*{url_part}*", timeout=timeout)
        else:
            expect(self.page).to_have_url(f"*{url_part}*")
    
    def get_text(self, selector: str) -> str:
        """取得元素文字內容。"""
        return self.page.locator(selector).text_content() or ""
    
    def get_input_value(self, selector: str) -> str:
        """取得輸入框的值。"""
        return self.page.locator(selector).input_value()
    
    def is_visible(self, selector: str) -> bool:
        """檢查元素是否可見。"""
        return self.page.locator(selector).is_visible()
    
    def wait_for_load_state(self, state: str = "domcontentloaded") -> None:
        """等待頁面載入狀態。"""
        self.page.wait_for_load_state(state)
    
    def select_option(self, selector: str, value: str) -> None:
        """從下拉選單選擇選項。"""
        self.page.locator(selector).select_option(value)
    
    def check(self, selector: str) -> None:
        """勾選 checkbox。"""
        self.page.locator(selector).check()
    
    def uncheck(self, selector: str) -> None:
        """取消勾選 checkbox。"""
        self.page.locator(selector).uncheck()
    
    def screenshot(self, path: str, full_page: bool = True) -> None:
        """擷取螢幕截圖。"""
        self.page.screenshot(path=path, full_page=full_page)
    
    def get_locator(self, selector: str) -> Locator:
        """取得元素 Locator。"""
        return self.page.locator(selector)
    
    def frame_locator(self, selector: str):
        """取得 iframe 的 FrameLocator。"""
        return self.page.frame_locator(selector)
