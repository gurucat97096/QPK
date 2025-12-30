"""
集中管理所有頁面的 Selectors。
待實作的 selector 請根據實際 HTML 更新。
"""


class LoginPageSelectors:
    """登入頁面 selectors。"""
    
    LOGIN_MODAL = "#loginModal"
    EMAIL_INPUT = "#loginFormEmail"
    PASSWORD_INPUT = "#loginFormPsw"
    AGREE_TERMS = "#agreeMemberTermsLogin"
    LOGIN_BUTTON = "#loginBtn"
    RECAPTCHA_TOKEN = "#reCAPTCHA_Token"
    
    # reCAPTCHA iframe 與 checkbox
    RECAPTCHA_ANCHOR_IFRAME = "iframe[src*='recaptcha/api2/anchor']"
    RECAPTCHA_CHECKBOX = "#recaptcha-anchor"
    
    # 特定驗證錯誤 selectors（避免 broad selector 造成 strict mode 問題）
    RECAPTCHA_VALIDATION_ERROR = '#loginModal span[data-valmsg-for="reCAPTCHA_Token"].field-validation-error'
    EMAIL_VALIDATION_ERROR = '#loginModal span[data-valmsg-for="loginFormEmail"].field-validation-error'
    PASSWORD_VALIDATION_ERROR = '#loginModal span[data-valmsg-for="loginFormPsw"].field-validation-error'
    
    # Modal 內一般錯誤（多個符合時使用 .first）
    LOGIN_MODAL_ERRORS = "#loginModal .invalid-feedback.field-validation-error"
    
    # Toast 錯誤（swal2）- 整個 popup 容器
    SWAL_POPUP = ".swal2-popup"
    TOAST_ERROR = ".swal2-popup .swal2-html-container"


class HomePageSelectors:
    """首頁 selectors。"""
    
    HOME_READY_TEXT = "text=快速登入"
    QUICK_LOGIN_BUTTON = "a:has-text('快速登入')"
    POLICY_AGREE_BUTTON = "#policyModal button:has-text('我同意')"
    
    # 頁面載入指示器（全白畫面時可能出現的 loading overlay）
    LOADING_OVERLAY = ".loading, .loader, .spinner, [class*='loading'], [class*='loader']"


class QueryPageSelectors:
    """車牌查詢頁面 selectors（待實作）。"""
    
    PLATE_INPUT = "input[name='plate_no']"
    SEARCH_BUTTON = "button.search"
    RESULT_TABLE = "table.result-table"
    RESULT_ROWS = "table.result-table tbody tr"
    NO_RESULT_MESSAGE = ".no-result"


class PaymentSelectors:
    """繳費選擇頁面 selectors（待實作）。"""
    
    TICKET_CHECKBOXES = "input[type='checkbox'].ticket-select"
    TOTAL_AMOUNT = ".total-amount"
    PROCEED_BUTTON = "button.proceed-payment"


class PaymentFormSelectors:
    """繳費表單頁面 selectors（待實作）。"""
    
    PAYER_NAME = "input[name='payer_name']"
    PAYER_PHONE = "input[name='payer_phone']"
    PAYER_EMAIL = "input[name='payer_email']"
    SUBMIT_BUTTON = "button.submit-payment"


class CreditCardSelectors:
    """TapPay 信用卡 iframe/欄位 selectors（待實作）。"""
    
    CARD_NUMBER_IFRAME = "iframe[name='card-number']"
    CARD_NUMBER_INPUT = "input[name='cardnumber']"
    
    CARD_EXPIRY_IFRAME = "iframe[name='card-expiry']"
    CARD_EXPIRY_INPUT = "input[name='exp-date']"
    
    CARD_CVV_IFRAME = "iframe[name='card-cvv']"
    CARD_CVV_INPUT = "input[name='cvc']"
    
    PAY_BUTTON = "button.pay-now"


class ThreeDSSelectors:
    """TapPay 3DS 驗證頁面 selectors（待實作）。"""
    
    VERIFICATION_IFRAME = "iframe.tappay-3ds"
    OTP_INPUT = "input[name='otp']"
    SUBMIT_OTP_BUTTON = "button.submit-otp"


class SuccessPageSelectors:
    """繳費成功頁面 selectors（待實作）。"""
    
    SUCCESS_MESSAGE = ".payment-success"
    TRANSACTION_ID = ".transaction-id"
    RECEIPT_BUTTON = "button.download-receipt"


class FooterNavSelectors:
    """底部導航欄 selectors。"""
    
    FOOTER = "footer.footer-fixed"
    HOME_LINK = "footer.footer-fixed a[href='/']"
    MEMBER_LINK = "footer.footer-fixed a[href='/Member/Home']"
    PARKING_TICKET_LINK = "footer.footer-fixed a[href='/ParkingTicket']"
    LIFE_DISCOUNT_LINK = "footer.footer-fixed a[href='/LifeDiscount']"


class ParkingTicketSelectors:
    """停車單頁面 selectors（根據實際頁面調整）。"""
    
    # 頁面標題/就緒指示
    PAGE_TITLE = "text=停車單"
    PAGE_READY = ".parking-ticket, [class*='ticket'], h1, h2"
    
    # 車號輸入區（路邊停車）
    CAR_NUMBER_INPUT = "#CarNumberID"
    SEARCH_BUTTON = "#btnGOrec"
    
    # 車牌輸入區（備用 selector）
    PLATE_INPUT = "#CarNumberID, input[placeholder*='車號'], input[placeholder*='車牌']"
    
    # 查詢結果
    TICKET_LIST = ".filter-content, .ticket-list, .parking-list"
    TICKET_CHECKBOX = "input.form-check-input[type='checkbox'][name='cbUnpaids']"
    FIRST_TICKET_CHECKBOX = "input.form-check-input[type='checkbox'][name='cbUnpaids']:first-of-type"
    NO_RESULT = "text=查無資料, text=無停車紀錄, .no-result"
    
    # 繳費相關
    PAY_BUTTON = "#myForm > footer > div > button"
    PAY_BUTTON_TEXT = "button:has-text('前往繳費')"
    SELECT_ALL = "input[type='checkbox'][id*='all'], .select-all"
    TOTAL_AMOUNT = ".total-amount, .amount, [class*='total']"


class CommonSelectors:
    """通用 selectors。"""
    
    LOADING_SPINNER = ".loading-spinner, .loading-mask, .spinner-border"
    LOADING_MASK = "#loadingDiv, .loading-mask"
    ERROR_ALERT = ".alert-error, .swal2-popup.swal2-icon-error"
    SUCCESS_ALERT = ".alert-success, .swal2-popup.swal2-icon-success"
    HEADER_LOGO = ".brand-logo img, header img[alt*='Qparking']"
    NAVIGATION_MENU = "nav.main-menu, footer.footer-fixed"
