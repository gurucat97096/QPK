# Parking Payment E2E Testing Framework

基於 Python + Playwright (Sync API) + pytest 的端到端測試專案。

## 目錄結構

```
QPK/
├── config/
│   ├── __init__.py
│   └── settings.py          # 環境變數設定
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # 基礎頁面物件
│   └── login_page.py         # 登入頁面物件
├── tests/
│   ├── __init__.py
│   └── test_payment_e2e.py   # E2E 測試案例
├── utils/
│   ├── __init__.py
│   └── selectors.py          # 集中管理的選擇器
├── artifacts/                 # 測試產出 (報告、截圖、traces)
│   ├── screenshots/
│   └── traces/
├── conftest.py               # pytest fixtures
├── pytest.ini                # pytest 設定
├── requirements.txt          # Python 依賴
├── Dockerfile                # Docker 映像檔
├── Jenkinsfile               # CI/CD Pipeline
├── .env.example              # 環境變數範本
└── .gitignore
```

## 快速開始

### 本地開發

1. **安裝依賴**
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **設定環境變數**
```bash
cp .env.example .env
# 編輯 .env 填入實際的測試帳號密碼
```

3. **執行測試**
```bash
# 執行所有測試
pytest

# 只執行 smoke 測試
pytest -m smoke

# 只執行 E2E 測試
pytest -m e2e

# 執行時顯示瀏覽器 (非 headless)
HEADLESS=false pytest
```

### Docker 執行

```bash
# 建構映像檔
docker build -t parking-e2e-tests .

# 執行測試
docker run --rm \
    -e BASE_URL="https://your-parking-site.com" \
    -e TEST_USERNAME="your_username" \
    -e TEST_PASSWORD="your_password" \
    -e PLATE_NO="AU-TO" \
    -v $(pwd)/artifacts:/app/artifacts \
    parking-e2e-tests
```

## 測試報告

測試完成後，報告會產生在 `artifacts/` 目錄：

- `artifacts/junit.xml` - JUnit XML 格式報告 (CI 整合用)
- `artifacts/report.html` - HTML 格式報告 (人工檢視用)
- `artifacts/screenshots/` - 失敗時的截圖
- `artifacts/traces/` - 失敗時的 Playwright trace (可用 `playwright show-trace trace.zip` 開啟)

## 環境變數

| 變數 | 說明 | 預設值 |
|------|------|--------|
| `BASE_URL` | 測試網站 URL | - |
| `TEST_USERNAME` | 測試帳號 | - |
| `TEST_PASSWORD` | 測試密碼 | - |
| `PLATE_NO` | 測試車牌號碼 | - |
| `CARD_NUMBER` | 測試信用卡號 | 4242424242424242 |
| `CARD_EXPIRY` | 信用卡到期日 | 12/28 |
| `CARD_CVV` | 信用卡安全碼 | 123 |
| `TAPPAY_3DS_CODE` | TapPay 3DS 驗證碼 | 1234567 |
| `HEADLESS` | 是否無頭模式 | true |
| `TIMEOUT` | 預設超時 (ms) | 30000 |

## 開發指南

### 更新選擇器

1. 取得實際網頁的 HTML
2. 更新 `utils/selectors.py` 中的選擇器常數
3. 移除 `# TODO: placeholder` 註解

### 新增頁面物件

1. 在 `pages/` 目錄新增 `your_page.py`
2. 繼承 `BasePage` 類別
3. 使用 `utils/selectors.py` 中的選擇器
4. 在 `pages/__init__.py` 中 export

### 新增測試案例

1. 在 `tests/` 目錄新增或修改測試檔案
2. 使用 pytest markers 標記測試類型 (`@pytest.mark.smoke`, `@pytest.mark.e2e`)
3. 使用 fixture 取得 page、credentials 等

## 重要規範

- ❌ **不要使用 `time.sleep()`** - 使用 Playwright 的 `expect()` 或明確等待
- ✅ 選擇器集中在 `utils/selectors.py`
- ✅ 敏感資料使用環境變數
- ✅ Page Object 模式封裝頁面操作
