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
    """繳費表單頁面 selectors。"""
    
    PAYER_NAME = "input[name='payer_name']"
    PAYER_PHONE = "input[name='payer_phone']"
    PAYER_EMAIL = "input[name='payer_email']"
    SUBMIT_BUTTON = "button.submit-payment"
    
    # 下一步按鈕
    PAYMENT_BUTTON = "#paymentButton"
    
    # 勾選未繳費項目
    CHECK_UNPAID = "#checkUnpaid"
    CHECK_UNPAID_BUTTON = "#checkUnpaidButton"
    
    # 選擇自行輸入信用卡資料的連結
    ENTER_CREDIT_CARD_LINK = "a.border-success:has-text('自行輸入信用卡資料')"


class CreditCardSelectors:
    """TapPay 信用卡欄位 selectors。"""
    
    # TapPay 欄位容器
    CARD_NUMBER_CONTAINER = "#tappay-card-number"
    CARD_EXPIRY_CONTAINER = "#tappay-expiration-date"
    CARD_CVV_CONTAINER = "#tappay-ccv"
    
    # TapPay iframe selectors (容器內的 iframe)
    CARD_NUMBER_IFRAME = "#tappay-card-number iframe"
    CARD_EXPIRY_IFRAME = "#tappay-expiration-date iframe"
    CARD_CVV_IFRAME = "#tappay-ccv iframe"
    
    # iframe 內部的輸入欄位 (精確 ID)
    CARD_NUMBER_INPUT = "#cc-number"
    CARD_EXPIRY_INPUT = "#cc-exp"
    CARD_CVV_INPUT = "#cc-ccv"
    
    # 確認送出按鈕
    PAYMENT_BUTTON = "#paymentButton"
    
    PAY_BUTTON = "button.pay-now"


class ThreeDSSelectors:
    """TapPay 3DS 驗證頁面 selectors。"""
    
    # OTP 輸入欄位
    OTP_INPUT = "#pin"
    
    # 送出按鈕
    SUBMIT_BUTTON = "#send"


class SuccessPageSelectors:
    """繳費成功頁面 selectors。"""
    
    # 繳費成功訊息
    SUCCESS_MESSAGE = "text=繳費成功"
    SUCCESS_TEXT = "繳費成功"
    
    # 備用 selectors
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
    
    # 付款方式下拉選單
    PAYMENT_METHOD_SELECT = "#PaymentMethod"
    PAYMENT_METHOD_CREDIT_CARD = "1"  # 信用卡
    PAYMENT_METHOD_LINE_PAY = "4"  # LINE Pay
    
    # 發票存入方式下拉選單
    INVOICE_OPTION_SELECT = "#InvoiceOptionString"
    INVOICE_OPTION_BARCODE = "1-/A3RUA54"  # 手機條碼載具
    INVOICE_OPTION_BARCODE_CUSTOM = "1"  # 手機條碼載具（自行輸入）
    INVOICE_OPTION_CITIZEN_DIGITAL = "2"  # 輸入統一編號
    INVOICE_OPTION_DONATION_919 = "4-919"  # 捐贈發票-愛心碼 919
    INVOICE_OPTION_DONATION_8585 = "4-8585"  # 捐贈發票-愛心碼 8585
    INVOICE_OPTION_DONATION_CUSTOM = "4"  # 捐贈發票自行輸入捐贈碼


class CommonSelectors:
    """通用 selectors。"""
    
    LOADING_SPINNER = ".loading-spinner, .loading-mask, .spinner-border"
    LOADING_MASK = "#loadingDiv, .loading-mask"
    ERROR_ALERT = ".alert-error, .swal2-popup.swal2-icon-error"
    SUCCESS_ALERT = ".alert-success, .swal2-popup.swal2-icon-success"
    HEADER_LOGO = ".brand-logo img, header img[alt*='Qparking']"
    NAVIGATION_MENU = "nav.main-menu, footer.footer-fixed"
