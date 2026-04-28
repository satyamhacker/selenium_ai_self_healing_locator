from __future__ import annotations

import os
import re
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DRIVER_ROOT = PROJECT_ROOT / ".drivers"
CHROMEDRIVER_NAME = "chromedriver.exe" if os.name == "nt" else "chromedriver"


def create_chrome_driver() -> webdriver.Chrome:
    options = Options()

    chrome_binary = _find_chrome_binary()
    if chrome_binary is not None:
        options.binary_location = str(chrome_binary)

    if os.getenv("SELENIUM_HEADLESS", "").lower() in {"1", "true", "yes"}:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")

    service = Service(executable_path=str(_ensure_matching_chromedriver(chrome_binary)))
    return webdriver.Chrome(service=service, options=options)


def _ensure_matching_chromedriver(chrome_binary: Path | None) -> Path:
    browser_version = _get_chrome_version(chrome_binary)
    driver_path = DRIVER_ROOT / browser_version / CHROMEDRIVER_NAME

    if driver_path.exists():
        return driver_path

    DRIVER_ROOT.mkdir(parents=True, exist_ok=True)
    version_dir = DRIVER_ROOT / browser_version
    version_dir.mkdir(parents=True, exist_ok=True)

    platform_key = "win64" if os.name == "nt" else "linux64"
    archive_name = f"chromedriver-{platform_key}.zip"
    download_url = (
        f"https://storage.googleapis.com/chrome-for-testing-public/"
        f"{browser_version}/{platform_key}/{archive_name}"
    )

    archive_path = version_dir / archive_name
    urllib.request.urlretrieve(download_url, archive_path)

    with zipfile.ZipFile(archive_path) as zip_file:
        zip_file.extractall(version_dir)

    extracted_driver = next(version_dir.rglob(CHROMEDRIVER_NAME), None)
    if extracted_driver is None:
        raise RuntimeError(
            f"Downloaded ChromeDriver for {browser_version}, but {CHROMEDRIVER_NAME} was not found."
        )

    shutil.copy2(extracted_driver, driver_path)
    archive_path.unlink(missing_ok=True)
    return driver_path


def _get_chrome_version(chrome_binary: Path | None) -> str:
    if chrome_binary is None:
        raise RuntimeError(
            "Chrome binary was not found. Install Google Chrome or set CHROME_BINARY to its path."
        )

    if os.name == "nt":
        powershell_command = (
            f"(Get-Item '{chrome_binary}').VersionInfo.ProductVersion"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", powershell_command],
            capture_output=True,
            text=True,
            check=True,
        )
        version_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", result.stdout.strip())
        if version_match is not None:
            return version_match.group(1)

    result = subprocess.run(
        [str(chrome_binary), "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    version_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", result.stdout or result.stderr)
    if version_match is None:
        raise RuntimeError(f"Could not detect Chrome version from: {result.stdout or result.stderr}")

    return version_match.group(1)


def _find_chrome_binary() -> Path | None:
    env_binary = os.getenv("CHROME_BINARY")
    if env_binary:
        binary_path = Path(env_binary)
        if binary_path.exists():
            return binary_path

    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path("/usr/bin/google-chrome"),
        Path("/usr/bin/google-chrome-stable"),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None
