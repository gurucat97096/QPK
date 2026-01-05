"""
應用程式設定，從環境變數載入。
本機開發使用 .env 檔，CI/CD 由環境變數注入。
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """測試套件設定。"""
    
    # 停車繳費網站 Base URL
    BASE_URL: str = os.getenv("BASE_URL", "https://qpktest.qparking.com.tw")
    
    # 登入帳密
    USERNAME: str = os.getenv("TEST_USERNAME", "tidcedgar@gmail.com")
    PASSWORD: str = os.getenv("TEST_PASSWORD", "edgar97096")
    
    # 測試資料
    PLATE_NO: str = os.getenv("PLATE_NO", "AU-TO")
    
    
    # 信用卡測試資料（TapPay 測試卡）
    CARD_NUMBER: str = os.getenv("CARD_NUMBER", "4242424242424242")
    CARD_EXPIRY: str = os.getenv("CARD_EXPIRY", "12/28")
    CARD_CVV: str = os.getenv("CARD_CVV", "123")
    
    # TapPay 3DS 驗證碼
    TAPPAY_3DS_CODE: str = os.getenv("TAPPAY_3DS_CODE", "1234567")
    
    # 瀏覽器設定
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))  # 毫秒
    
    @classmethod
    def validate(cls) -> None:
        """驗證必要設定是否存在。"""
        required = ["BASE_URL", "USERNAME", "PASSWORD", "PLATE_NO"]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"缺少必要的環境變數：{missing}")


settings = Settings()
