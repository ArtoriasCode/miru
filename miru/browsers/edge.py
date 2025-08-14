from typing import List

from miru.browsers.base import BaseBrowser


class EdgeBrowser(BaseBrowser):
    """
    Edge browser implementation.
    """
    NAME: str = "Edge"
    WIN_REG_PATH: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"
    MAC_APP_NAME: str = "Microsoft Edge.app"
    MAC_DEFAULT_PATH: str = r"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    MAC_ALTERNATIVE_PATH: str = "/Contents/MacOS/Microsoft Edge"
    LINUX_NAMES: List = [
        "microsoft-edge",
        "microsoft-edge-stable"
    ]
