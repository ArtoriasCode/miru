from typing import List

from miru.browsers.base import BaseBrowser


class ChromiumBrowser(BaseBrowser):
    """
    Chromium browser implementation.
    """
    NAME: str = "Chromium"
    WIN_REG_PATH: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
    MAC_APP_NAME: str = "Chromium.app"
    MAC_DEFAULT_PATH: str = r"/Applications/Chromium.app/Contents/MacOS/Chromium"
    MAC_ALTERNATIVE_PATH: str = "/Contents/MacOS/Chromium"
    LINUX_NAMES: List = [
        "chromium-browser",
        "chromium"
    ]
