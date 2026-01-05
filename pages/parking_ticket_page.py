"""
停車單頁面 Page Object。
"""
import re
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from utils.selectors import FooterNavSelectors, ParkingTicketSelectors, CommonSelectors


class ParkingTicketPage(BasePage):
    """停車單頁面 Page Object。"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url
        self.selectors = ParkingTicketSelectors
        self.footer = FooterNavSelectors
        self.common = CommonSelectors
    
    def navigate(self) -> "ParkingTicketPage":
        """直接導航至停車單頁面。"""
        self.goto(f"{self.base_url}/ParkingTicket")
        self.wait_page_ready()
        return self
    
    def navigate_from_footer(self) -> "ParkingTicketPage":
        """從底部導航欄點擊進入停車單頁面。"""
        self.click(self.footer.PARKING_TICKET_LINK)
        self.wait_page_ready()
        return self
    
    def wait_page_ready(self, timeout: int = 15000) -> None:
        """等待停車單頁面載入完成。"""
        # 等待 DOM 載入
        self.page.wait_for_load_state("domcontentloaded")
        
        # 等待 loading mask 消失
        try:
            loading = self.page.locator(self.common.LOADING_MASK)
            if loading.count() > 0 and loading.first.is_visible():
                loading.first.wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass
        
        # 等待網路請求完成
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except PlaywrightTimeoutError:
            pass
    
    def wait_for_url(self, timeout: int = 10000) -> None:
        """等待 URL 變更為 /ParkingTicket。"""
        self.page.wait_for_url("**/ParkingTicket**", timeout=timeout)
    
    def enter_plate_number(self, plate_no: str) -> "ParkingTicketPage":
        """輸入車牌號碼。"""
        # 等待輸入框可見
        input_locator = self.page.locator(self.selectors.CAR_NUMBER_INPUT)
        input_locator.wait_for(state="visible", timeout=10000)
        # 使用 fill 方法填入車牌
        input_locator.fill(plate_no)
        return self
    
    def click_search(self) -> "ParkingTicketPage":
        """點擊查詢車號按鈕。"""
        # 等待按鈕可見並點擊
        btn_locator = self.page.locator(self.selectors.SEARCH_BUTTON)
        btn_locator.wait_for(state="visible", timeout=10000)
        btn_locator.click()
        return self
    
    def search_plate(self, plate_no: str) -> "ParkingTicketPage":
        """輸入車號並查詢。"""
        self.enter_plate_number(plate_no)
        self.click_search()
        self.wait_page_ready()
        return self
    
    def has_results(self) -> bool:
        """檢查是否有查詢結果。"""
        try:
            ticket_items = self.page.locator(self.selectors.TICKET_ITEM)
            return ticket_items.count() > 0
        except Exception:
            return False
    
    def has_no_result_message(self) -> bool:
        """檢查是否顯示無結果訊息。"""
        try:
            no_result = self.page.locator(self.selectors.NO_RESULT)
            return no_result.is_visible()
        except Exception:
            return False
    
    def get_ticket_count(self) -> int:
        """取得停車單數量。"""
        return self.page.locator(self.selectors.TICKET_CHECKBOX).count()
    
    def select_first_ticket(self) -> "ParkingTicketPage":
        """選擇第一筆停車單。"""
        checkbox = self.page.locator(self.selectors.TICKET_CHECKBOX).first
        checkbox.wait_for(state="visible", timeout=10000)
        if not checkbox.is_checked():
            checkbox.click()
        return self
    
    def select_ticket(self, index: int = 0) -> "ParkingTicketPage":
        """選擇指定索引的停車單（預設第一筆）。"""
        checkboxes = self.page.locator(self.selectors.TICKET_CHECKBOX)
        if checkboxes.count() > index:
            checkbox = checkboxes.nth(index)
            if not checkbox.is_checked():
                checkbox.click()
        return self
    
    def select_all_tickets(self) -> "ParkingTicketPage":
        """選擇全部停車單。"""
        select_all = self.page.locator(self.selectors.SELECT_ALL)
        if select_all.count() > 0 and not select_all.is_checked():
            select_all.check()
        return self
    
    def click_pay(self) -> None:
        """點擊前往繳費按鈕。"""
        pay_btn = self.page.locator(self.selectors.PAY_BUTTON)
        pay_btn.wait_for(state="visible", timeout=10000)
        pay_btn.click()
    
    def select_payment_method(self, method: str = "credit_card") -> "ParkingTicketPage":
        """選擇付款方式。
        
        Args:
            method: 付款方式，可選 'credit_card' 或 'line_pay'
        """
        select_locator = self.page.locator(self.selectors.PAYMENT_METHOD_SELECT)
        select_locator.wait_for(state="visible", timeout=10000)
        
        if method == "credit_card":
            select_locator.select_option(value=self.selectors.PAYMENT_METHOD_CREDIT_CARD)
        elif method == "line_pay":
            select_locator.select_option(value=self.selectors.PAYMENT_METHOD_LINE_PAY)
        else:
            select_locator.select_option(value=method)
        
        return self
    
    def select_invoice_option(self, option: str = "barcode") -> "ParkingTicketPage":
        """選擇發票存入方式。
        
        Args:
            option: 發票存入方式，可選:
                - 'barcode': 手機條碼載具（預設載具）
                - 'barcode_custom': 手機條碼載具（自行輸入）
                - 'citizen_digital': 輸入統一編號
                - 'donation_919': 捐贈發票-愛心碼 919-創世基金會
                - 'donation_8585': 捐贈發票-愛心碼 8585-家扶基金會
                - 'donation_custom': 捐贈發票自行輸入捐贈碼
        """
        select_locator = self.page.locator(self.selectors.INVOICE_OPTION_SELECT)
        select_locator.wait_for(state="visible", timeout=10000)
        
        option_map = {
            "barcode": self.selectors.INVOICE_OPTION_BARCODE,
            "barcode_custom": self.selectors.INVOICE_OPTION_BARCODE_CUSTOM,
            "citizen_digital": self.selectors.INVOICE_OPTION_CITIZEN_DIGITAL,
            "donation_919": self.selectors.INVOICE_OPTION_DONATION_919,
            "donation_8585": self.selectors.INVOICE_OPTION_DONATION_8585,
            "donation_custom": self.selectors.INVOICE_OPTION_DONATION_CUSTOM,
        }
        
        value = option_map.get(option, option)
        select_locator.select_option(value=value)
        
        return self
    
    def get_total_amount(self) -> str:
        """取得應繳總金額文字。"""
        return self.page.locator(self.selectors.TOTAL_AMOUNT).text_content() or ""
    
    def assert_on_parking_ticket_page(self) -> None:
        """斷言已在停車單頁面。"""
        expect(self.page).to_have_url(re.compile(r".*ParkingTicket.*"), timeout=10000)
