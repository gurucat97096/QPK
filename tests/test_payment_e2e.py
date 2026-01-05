"""
停車繳費網站 E2E 測試。

測試流程：
1. 登入
2. 導航至停車單頁面
3. 查詢車牌
4. 勾選繳費單
5. 填寫繳費資訊
6. 輸入信用卡（TapPay 測試卡 4242）
7. 完成 3DS 驗證（驗證碼：1234567）
8. 驗證成功畫面
"""
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.parking_ticket_page import ParkingTicketPage
from config.settings import settings


class TestPaymentE2E:
    """停車繳費流程端對端測試。"""
    
    @pytest.mark.smoke
    def test_login_success(
        self,
        page: Page,
        base_url: str,
        test_credentials: dict,
    ) -> None:
        """冒煙測試：驗證使用者可成功登入。"""
        login_page = LoginPage(page, base_url)
        
        login_page.navigate()
        login_page.login(
            email=test_credentials["username"],
            password=test_credentials["password"],
        )
        login_page.assert_login_success()
    
    @pytest.mark.smoke
    def test_navigate_to_parking_ticket(
        self,
        page: Page,
        base_url: str,
        test_credentials: dict,
        test_data: dict,
    ) -> None:
        """冒煙測試：登入後進入停車單頁面並查詢車號。"""
        # 步驟 1：登入
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        login_page.login(
            email=test_credentials["username"],
            password=test_credentials["password"],
        )
        login_page.assert_login_success()
        
        # 步驟 2：點擊底部導航進入停車單頁面
        parking_page = ParkingTicketPage(page, base_url)
        parking_page.navigate_from_footer()
        parking_page.assert_on_parking_ticket_page()
        
        # 步驟 3：輸入車號並查詢
        plate_no = test_data.get("plate_no", "ABC1234")
        parking_page.enter_plate_number(plate_no)
        parking_page.click_search()
        
        # 步驟 4：選擇第一筆停車單
        parking_page.select_first_ticket()
        
        # 步驟 5：點擊前往繳費
        parking_page.click_pay()
        
        # 步驟 6：選擇付款方式 - 信用卡
        parking_page.select_payment_method("credit_card")
        
        # 步驟 7：選擇發票存入方式 - 手機條碼載具
        parking_page.select_invoice_option("barcode")
    
    @pytest.mark.e2e
    @pytest.mark.payment
    def test_full_payment_flow(
        self,
        page: Page,
        base_url: str,
        test_credentials: dict,
        test_data: dict,
    ) -> None:
        """
        完整 E2E 測試：從登入到繳費成功的完整流程。
        
        流程：登入 → 進入停車單頁面 → 查詢車牌 → 勾選繳費單 → 填寫資訊 → 輸入信用卡 → 3DS 驗證 → 成功畫面
        """
        # 步驟 1：登入
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        login_page.login(
            email=test_credentials["username"],
            password=test_credentials["password"],
        )
        login_page.assert_login_success()
        
        # 步驟 2：進入停車單頁面
        parking_page = ParkingTicketPage(page, base_url)
        parking_page.navigate_from_footer()
        parking_page.assert_on_parking_ticket_page()
        
        # 步驟 3-8：待實作（需先確認實際頁面結構）
        pytest.skip("待實作：車牌查詢與繳費步驟 - 請先確認實際頁面 selectors")
    
    @pytest.mark.e2e
    def test_query_plate_no_results(
        self,
        page: Page,
        base_url: str,
        test_credentials: dict,
    ) -> None:
        """測試：查詢無停車紀錄的車牌。"""
        # 步驟 1：登入
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        login_page.login(
            email=test_credentials["username"],
            password=test_credentials["password"],
        )
        login_page.assert_login_success()
        
        # 步驟 2：進入停車單頁面
        parking_page = ParkingTicketPage(page, base_url)
        parking_page.navigate_from_footer()
        parking_page.assert_on_parking_ticket_page()
        
        # 步驟 3：查詢一個不存在的車牌
        pytest.skip("待實作：查無結果測試 - 需確認頁面 selectors")
