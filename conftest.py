"""
Pytest 設定與 fixtures。
提供瀏覽器、context、page fixtures，支援 tracing、截圖、錄影與 console log。
"""
import os
import re
import shutil
import pytest
from datetime import datetime
from pathlib import Path
from typing import Generator, List, Dict, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright

from config.settings import settings


# 產出物目錄
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
TRACES_DIR = ARTIFACTS_DIR / "traces"
LOGS_DIR = ARTIFACTS_DIR / "logs"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
VIDEOS_RAW_DIR = VIDEOS_DIR / "raw"

# Trace 編號計數器（session-level）
_trace_counter = 0

# 暫存每個測試的 artifacts 資訊（用於 teardown 後處理）
_test_artifacts: Dict[str, Dict[str, Any]] = {}


def _safe_filename(nodeid: str) -> str:
    """將 pytest nodeid 轉換為安全的檔名。"""
    safe_name = re.sub(r'[:\\/\s\[\]<>"|?*]', '_', nodeid)
    safe_name = re.sub(r'_+', '_', safe_name)
    safe_name = safe_name.strip('_')
    if len(safe_name) > 200:
        safe_name = safe_name[:200]
    return safe_name


def pytest_configure(config: pytest.Config) -> None:
    """測試執行前建立產出物目錄，並從現有檔案取得最大編號。"""
    global _trace_counter
    
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    TRACES_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    VIDEOS_DIR.mkdir(exist_ok=True)
    VIDEOS_RAW_DIR.mkdir(exist_ok=True)
    
    # 掃描現有 artifacts 取得最大編號，下次從這個編號繼續
    max_num = 0
    for directory in [TRACES_DIR, LOGS_DIR, SCREENSHOTS_DIR, VIDEOS_DIR]:
        if directory.exists():
            for f in directory.iterdir():
                if f.is_file():
                    # 檔名格式: 001_PASS_xxx 或 001_FAIL_xxx
                    match = re.match(r'^(\d{3})_', f.name)
                    if match:
                        num = int(match.group(1))
                        if num > max_num:
                            max_num = num
    
    _trace_counter = max_num
    if max_num > 0:
        print(f"\n[conftest] 偵測到現有 artifacts，編號將從 {max_num + 1:03d} 開始")


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """建立測試 session 的 Playwright 實例。"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """建立測試 session 的瀏覽器實例。"""
    browser = playwright_instance.chromium.launch(
        headless=settings.HEADLESS,
        slow_mo=settings.SLOW_MO,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """為每個測試建立瀏覽器 context，啟用 tracing 與錄影。"""
    global _trace_counter
    _trace_counter += 1
    current_num = _trace_counter
    
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-TW",
        timezone_id="Asia/Taipei",
        # 錄影設定
        record_video_dir=str(VIDEOS_RAW_DIR),
        record_video_size={"width": 1920, "height": 1080},
    )
    
    # 防止 main.js 因 unreadCountURL is not defined 噴錯，造成首屏白畫面
    context.add_init_script("window.unreadCountURL = window.unreadCountURL || '';")
    
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    
    # 儲存 artifacts 資訊供後續使用
    _test_artifacts[request.node.nodeid] = {
        "trace_num": current_num,
        "safe_name": _safe_filename(request.node.nodeid),
        "video_path": None,
    }
    
    yield context
    
    # Tracing：都要保留，但此時還不知道 pass/fail，先用暫存名稱
    # 最終名稱在 pytest_runtest_makereport 後處理
    temp_trace_path = TRACES_DIR / f"{current_num:03d}_PENDING_{_safe_filename(request.node.nodeid)}_trace.zip"
    context.tracing.stop(path=str(temp_trace_path))
    _test_artifacts[request.node.nodeid]["trace_path"] = temp_trace_path
    
    context.close()


def _is_test_failed(node) -> bool:
    """判斷測試是否失敗（包含 setup 失敗）。"""
    rep_call = getattr(node, "rep_call", None)
    rep_setup = getattr(node, "rep_setup", None)
    return (rep_setup and rep_setup.failed) or (rep_call and rep_call.failed)


def _get_test_outcome(node) -> str:
    """取得測試結果字串。"""
    rep_call = getattr(node, "rep_call", None)
    rep_setup = getattr(node, "rep_setup", None)
    
    if rep_setup and rep_setup.failed:
        return "setup_failure"
    elif rep_call is None:
        return "unknown"
    elif rep_call.failed:
        return "failed"
    elif rep_call.skipped:
        return "skipped"
    elif rep_call.passed:
        return "passed"
    return "unknown"


@pytest.fixture(scope="function")
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    """為每個測試建立 page，收集 console/error log。"""
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    
    # 收集 console / pageerror / requestfailed 事件
    log_entries: List[Dict[str, Any]] = []
    test_start_time = datetime.now()
    
    def on_console(msg):
        try:
            location = msg.location
            log_entries.append({
                "time": datetime.now().isoformat(),
                "type": "console",
                "level": msg.type,
                "text": msg.text,
                "url": location.get("url", "") if location else "",
                "line": location.get("lineNumber", "") if location else "",
                "column": location.get("columnNumber", "") if location else "",
            })
        except Exception:
            log_entries.append({
                "time": datetime.now().isoformat(),
                "type": "console",
                "level": msg.type,
                "text": msg.text,
                "url": "",
                "line": "",
                "column": "",
            })
    
    def on_pageerror(error):
        log_entries.append({
            "time": datetime.now().isoformat(),
            "type": "pageerror",
            "message": str(error),
        })
    
    def on_requestfailed(req):
        try:
            failure = req.failure
            log_entries.append({
                "time": datetime.now().isoformat(),
                "type": "requestfailed",
                "url": req.url,
                "failure": failure if failure else "unknown",
            })
        except Exception:
            log_entries.append({
                "time": datetime.now().isoformat(),
                "type": "requestfailed",
                "url": req.url,
                "failure": "unknown",
            })
    
    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    page.on("requestfailed", on_requestfailed)
    
    yield page
    
    # === Teardown ===
    nodeid = request.node.nodeid
    artifacts = _test_artifacts.get(nodeid, {})
    safe_name = artifacts.get("safe_name", _safe_filename(nodeid))
    trace_num = artifacts.get("trace_num", 0)
    
    # 先截圖（暫存），之後根據結果決定是否保留
    temp_screenshot_path = None
    try:
        if not page.is_closed():
            temp_screenshot_path = SCREENSHOTS_DIR / f"temp_{trace_num:03d}_{safe_name}.png"
            page.screenshot(path=str(temp_screenshot_path), full_page=True)
    except Exception:
        pass
    _test_artifacts[nodeid]["screenshot_path"] = temp_screenshot_path
    
    # 取得影片路徑（必須在 page.close() 之前）
    try:
        if page.video:
            _test_artifacts[nodeid]["video_path"] = page.video.path()
    except Exception:
        pass
    
    # 儲存 log 資訊供後續使用
    _test_artifacts[nodeid]["log_entries"] = log_entries
    _test_artifacts[nodeid]["test_start_time"] = test_start_time
    
    # 關閉 page
    try:
        if not page.is_closed():
            page.close()
    except Exception:
        pass


def _handle_video(video_path: str | None, safe_name: str, test_failed: bool, trace_num: int) -> None:
    """處理影片：失敗時保留並重新命名（加編號），否則刪除。"""
    if not video_path:
        return
    
    try:
        video_file = Path(video_path)
        # 等待影片寫入完成
        import time
        for _ in range(10):
            if video_file.exists():
                break
            time.sleep(0.1)
        
        if not video_file.exists():
            return
        
        if test_failed:
            # 移動到 videos 目錄並重新命名，加上編號
            dest_path = VIDEOS_DIR / f"{trace_num:03d}_FAIL_{safe_name}.webm"
            shutil.move(str(video_file), str(dest_path))
            print(f"影片已儲存：{dest_path}")
        else:
            # 刪除影片
            video_file.unlink(missing_ok=True)
            print(f"影片已刪除（PASS）：{video_file.name}")
    except Exception as e:
        print(f"處理影片失敗 {safe_name}：{e}")


def _save_log_file(
    nodeid: str,
    outcome: str,
    start_time: datetime,
    log_entries: List[Dict[str, Any]],
    safe_name: str,
    trace_num: int = 0,
) -> None:
    """儲存 console/pageerror log 檔案。"""
    try:
        outcome_label = "FAIL" if outcome in ("failed", "setup_failure") else "PASS"
        log_path = LOGS_DIR / f"{trace_num:03d}_{outcome_label}_{safe_name}.log"
        
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"{'=' * 60}\n")
            f.write(f"Test: {nodeid}\n")
            f.write(f"Outcome: {outcome}\n")
            f.write(f"Start Time: {start_time.isoformat()}\n")
            f.write(f"End Time: {datetime.now().isoformat()}\n")
            f.write(f"{'=' * 60}\n\n")
            
            if not log_entries:
                f.write("(No console/error events captured)\n")
            else:
                for entry in log_entries:
                    entry_type = entry.get("type", "unknown")
                    timestamp = entry.get("time", "")
                    
                    if entry_type == "console":
                        level = entry.get("level", "log")
                        text = entry.get("text", "")
                        url = entry.get("url", "")
                        line = entry.get("line", "")
                        col = entry.get("column", "")
                        
                        location = ""
                        if url:
                            location = f" @ {url}"
                            if line:
                                location += f":{line}"
                                if col:
                                    location += f":{col}"
                        
                        f.write(f"[{timestamp}] CONSOLE.{level.upper()}: {text}{location}\n")
                    
                    elif entry_type == "pageerror":
                        message = entry.get("message", "")
                        f.write(f"[{timestamp}] PAGE_ERROR: {message}\n")
                    
                    elif entry_type == "requestfailed":
                        url = entry.get("url", "")
                        failure = entry.get("failure", "")
                        f.write(f"[{timestamp}] REQUEST_FAILED: {url} - {failure}\n")
                    
                    else:
                        f.write(f"[{timestamp}] {entry_type.upper()}: {entry}\n")
            
            f.write(f"\n{'=' * 60}\n")
            f.write(f"Total events: {len(log_entries)}\n")
        
        # 不印出 log 路徑以減少輸出雜訊，只在失敗時提示
        if outcome in ("failed", "setup_failure"):
            print(f"Log 已儲存：{log_path}")
    
    except Exception as e:
        print(f"儲存 log 失敗 {safe_name}：{e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """擷取測試結果並儲存於 test item，以便後續處理 artifacts。"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    
    # 在 teardown 階段完成後處理 artifacts
    if rep.when == "teardown":
        _process_artifacts_after_test(item)


def _process_artifacts_after_test(item: pytest.Item) -> None:
    """測試完全結束後處理 artifacts（screenshot、video、trace、log）。"""
    nodeid = item.nodeid
    artifacts = _test_artifacts.get(nodeid, {})
    
    if not artifacts:
        return
    
    trace_num = artifacts.get("trace_num", 0)
    safe_name = artifacts.get("safe_name", _safe_filename(nodeid))
    video_path = artifacts.get("video_path")
    trace_path = artifacts.get("trace_path")
    screenshot_path = artifacts.get("screenshot_path")
    log_entries = artifacts.get("log_entries", [])
    test_start_time = artifacts.get("test_start_time", datetime.now())
    
    # 判斷測試結果
    test_failed = _is_test_failed(item)
    outcome = _get_test_outcome(item)
    outcome_label = "FAIL" if test_failed else "PASS"
    
    # 1. Trace：重新命名加上 PASS/FAIL 標籤
    if trace_path and Path(trace_path).exists():
        final_trace_path = TRACES_DIR / f"{trace_num:03d}_{outcome_label}_{safe_name}_trace.zip"
        try:
            shutil.move(str(trace_path), str(final_trace_path))
            print(f"Trace 已儲存：{final_trace_path}")
        except Exception as e:
            print(f"Trace 重新命名失敗：{e}")
    
    # 2. 截圖：只有失敗才保留，否則刪除
    if screenshot_path and Path(screenshot_path).exists():
        if test_failed:
            final_screenshot_path = SCREENSHOTS_DIR / f"{trace_num:03d}_FAIL_{safe_name}.png"
            try:
                shutil.move(str(screenshot_path), str(final_screenshot_path))
                print(f"截圖已儲存：{final_screenshot_path}")
            except Exception as e:
                print(f"截圖重新命名失敗：{e}")
        else:
            try:
                Path(screenshot_path).unlink(missing_ok=True)
            except Exception:
                pass
    
    # 3. 影片：只有失敗才保留，否則刪除
    if video_path:
        _handle_video(video_path, safe_name, test_failed, trace_num)
    
    # 4. Log：永遠儲存
    _save_log_file(nodeid, outcome, test_start_time, log_entries, safe_name, trace_num)
    
    # 清理暫存
    if nodeid in _test_artifacts:
        del _test_artifacts[nodeid]


@pytest.fixture(scope="session")
def base_url() -> str:
    """回傳測試目標網站的 Base URL。"""
    return settings.BASE_URL


@pytest.fixture(scope="session")
def test_credentials() -> dict:
    """回傳測試用帳密。"""
    return {
        "username": settings.USERNAME,
        "password": settings.PASSWORD,
    }


@pytest.fixture(scope="session")
def test_data() -> dict:
    """回傳測試資料。"""
    return {
        "plate_no": settings.PLATE_NO,
        "card_number": settings.CARD_NUMBER,
        "card_expiry": settings.CARD_EXPIRY,
        "card_cvv": settings.CARD_CVV,
        "tappay_3ds_code": settings.TAPPAY_3DS_CODE,
    }
