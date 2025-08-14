from typing import List

from miru.browsers.base import BaseBrowser


class ChromeBrowser(BaseBrowser):
    """
    Chrome browser implementation.
    """
    NAME: str = "Chrome"
    WIN_REG_PATH: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
    MAC_APP_NAME: str = "Google Chrome.app"
    MAC_DEFAULT_PATH: str = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    MAC_ALTERNATIVE_PATH: str = "/Contents/MacOS/Google Chrome"
    LINUX_NAMES: List = [
        "google-chrome-stable",
        "google-chrome"
    ]
