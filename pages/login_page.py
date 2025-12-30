"""
登入頁面 Page Object。
"""
from playwright.sync_api import Page, Response, expect, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from utils.selectors import HomePageSelectors, LoginPageSelectors


class LoginPage(BasePage):
    """登入頁面 Page Object。"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.selectors = LoginPageSelectors
        self.last_login_response: Response | None = None
    
    def navigate(self) -> "LoginPage":
        """導航至訪客入口頁面，等待頁面完全載入。"""
        self.goto(f"{self.base_url}/visitor")
        self.wait_visitor_ready()
        return self
    
    def wait_visitor_ready(self, timeout: int = 15000) -> None:
        """
        等待訪客頁面完全載入並可互動。
        
        流程：
        1. 等待 DOM 載入完成
        2. 等待 document.readyState === 'complete'
        3. 等待可互動元素出現（快速登入按鈕）
        4. 若有 loading overlay 則等待其消失
        """
        # 1. 等待 DOM 載入完成
        self.page.wait_for_load_state("domcontentloaded")
        
        # 2. 等待 document.readyState === 'complete'
        try:
            self.page.wait_for_function(
                "document.readyState === 'complete'",
                timeout=timeout
            )
        except PlaywrightTimeoutError:
            pass  # 繼續執行，不要因此失敗
        
        # 3. 等待可互動元素出現（快速登入按鈕）
        try:
            quick_login_btn = self.page.locator(HomePageSelectors.QUICK_LOGIN_BUTTON)
            expect(quick_login_btn).to_be_visible(timeout=timeout)
        except Exception:
            # 嘗試備用元素
            try:
                home_ready = self.page.locator(HomePageSelectors.HOME_READY_TEXT)
                expect(home_ready).to_be_visible(timeout=5000)
            except Exception:
                pass  # 元素未出現，繼續執行
        
        # 4. 若有 loading overlay 則等待其消失（可選，不強制）
        if hasattr(HomePageSelectors, 'LOADING_OVERLAY') and HomePageSelectors.LOADING_OVERLAY:
            try:
                loading = self.page.locator(HomePageSelectors.LOADING_OVERLAY)
                if loading.count() > 0:
                    loading.first.wait_for(state="hidden", timeout=8000)
            except Exception:
                pass  # loading overlay 不存在或已消失，不影響流程
    
    def wait_home_ready(self, timeout: int = 15000) -> None:
        """等待首頁就緒（快速登入按鈕可見），處理初始載入延遲。"""
        # 先等待 DOM 載入完成
        self.page.wait_for_load_state("domcontentloaded")
        # 等待快速登入按鈕出現
        self.wait_visible(HomePageSelectors.HOME_READY_TEXT, timeout=timeout)
    
    def open_login_modal(self) -> None:
        """透過快速登入開啟登入 Modal 並同意政策。"""
        self.click(HomePageSelectors.QUICK_LOGIN_BUTTON)
        self.wait_visible("#policyModal")
        self.click(HomePageSelectors.POLICY_AGREE_BUTTON)
        self.wait_visible(self.selectors.LOGIN_MODAL)
    
    def enter_email(self, email: str) -> "LoginPage":
        """填入電子郵件。"""
        self.fill(self.selectors.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password: str) -> "LoginPage":
        """填入密碼。"""
        self.fill(self.selectors.PASSWORD_INPUT, password)
        return self
    
    def agree_terms(self) -> None:
        """勾選同意條款。"""
        checkbox = self.page.locator(self.selectors.AGREE_TERMS)
        if not checkbox.is_checked():
            checkbox.check()
    
    def click_login_button(self) -> None:
        """點擊登入按鈕（不等待 API 回應）。"""
        self.click(self.selectors.LOGIN_BUTTON)

    def submit_login_and_wait_for_response(self, timeout: int = 15000) -> Response | None:
        """
        點擊登入並等待 LoginApi 回應。
        
        Raises:
            AssertionError: 若逾時未收到 API 回應
        """
        self.last_login_response = None
        
        try:
            with self.page.expect_response(
                lambda r: "/Login/LoginApi" in r.url,
                timeout=timeout,
            ) as resp_info:
                self.click_login_button()
            self.last_login_response = resp_info.value
            return self.last_login_response
        except PlaywrightTimeoutError:
            raise AssertionError(f"登入 API 逾時（{timeout}ms 內未收到 /Login/LoginApi 回應）")

    def login(self, email: str, password: str) -> None:
        """
        執行完整登入流程：開 Modal → 填寫帳密 → 同意條款 → 送出。
        
        Raises:
            AssertionError: 若登入 API 逾時
        """
        self.wait_home_ready()
        self.open_login_modal()
        self.enter_email(email)
        self.enter_password(password)
        self.agree_terms()
        self.page.wait_for_timeout(300)
        self.submit_login_and_wait_for_response()
        try:
            expect(self.page.locator(self.selectors.LOGIN_MODAL)).to_be_hidden(timeout=15000)
        except PlaywrightTimeoutError:
            pass
    
    def login_and_navigate(self, email: str, password: str) -> None:
        """導航至首頁並執行登入。"""
        self.navigate()
        self.login(email, password)
    
    def assert_login_success(self) -> None:
        """斷言登入成功（Modal 隱藏、API 回應正常）。"""
        if self.last_login_response is not None and not self.last_login_response.ok:
            raise AssertionError(f"登入 API 失敗：status={self.last_login_response.status}")
        expect(self.page.locator(self.selectors.LOGIN_MODAL)).to_be_hidden(timeout=15000)
