from os import path
from abc import ABC
from sys import platform
from shutil import which
from subprocess import check_output
from subprocess import Popen, PIPE
from typing import Optional, List

from miru.utils.dataclasses import AppConfig


class BaseBrowser(ABC):
    """
    Base class for browser implementations.
    """
    NAME: str = "Base"
    WIN_REG_PATH: str = None
    MAC_APP_NAME: str = None
    MAC_DEFAULT_PATH: str = None
    MAC_ALTERNATIVE_PATH: str = None
    LINUX_NAMES: List = None

    def _find_mac(self) -> Optional[str]:
        """
        Looking for the path to browser on Mac.

        Parameters:
        - None.

        Returns:
        - str: Browser executable path.
        """
        if path.exists(self.MAC_DEFAULT_PATH):
            return self.MAC_DEFAULT_PATH

        try:
            output = check_output(["mdfind", self.MAC_APP_NAME]).decode()

            for line in output.split("\n"):
                if line.endswith(self.MAC_DEFAULT_PATH):
                    return line + self.MAC_ALTERNATIVE_PATH
        except Exception:
            return None

        return None

    def _find_linux(self) -> Optional[str]:
        """
        Looking for the path to browser on Linux.

        Parameters:
        - None.

        Returns:
        - str: Browser executable path.
        """
        for name in self.LINUX_NAMES:
            chrome_path = which(name)

            if chrome_path:
                return chrome_path

        return None

    def _find_win(self) -> Optional[str]:
        """
        Looking for the path to browser on Windows.

        Parameters:
        - None.

        Returns:
        - str: Browser executable path.
        """
        import winreg as reg

        try:
            for root in (reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE):
                try:
                    key = reg.OpenKey(root, self.WIN_REG_PATH, 0, reg.KEY_READ)
                    chrome_path = reg.QueryValue(key, None).strip('"').strip('\'')
                    reg.CloseKey(key)

                    if path.exists(chrome_path) and path.isfile(chrome_path):
                        return chrome_path
                except FileNotFoundError:
                    continue

        except Exception:
            return None

        return None

    def find_path(self) -> Optional[str]:
        """
        Looking for the path to browser depending on the system.

        Parameters:
        - None.

        Returns:
        - str: Browser executable path.
        """
        if platform in ["win32", "win64"]:
            return self._find_win()

        elif platform == "darwin":
            return self._find_mac()

        elif platform.startswith("linux"):
            return self._find_linux()

        return None

    def launch(self, page: str, config: AppConfig) -> None:
        """
        Launches the browser as an application.

        Parameters:
        - page: Page to launch.
        - config: App config object.

        Returns:
        - None.
        """
        browser_path = self.find_path()

        if not browser_path:
            raise EnvironmentError(f"{self.NAME} browser not found")

        url = f"http://{config.host}:{config.port}/{page}"
        args = config.cmd_args[:]

        size = config.window_size

        if size:
            width, height = size
            args.append(f'--window-size={width},{height}')

        position = config.window_position

        if position:
            x, y = position
            args.append(f'--window-position={x},{y}')

        Popen([browser_path, f'--app={url}'] + args, stdout=PIPE, stderr=PIPE, stdin=PIPE)
