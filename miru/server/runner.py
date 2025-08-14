from os import path
from threading import Timer
from typing import Tuple, List

from bottle import run
from bottle_websocket import GeventWebSocketServer

from miru.misc import app
from miru.server.utils import wait_for_server
from miru.server.routes import router as routes_router
from miru.server.websockets import router as websockets_router
from miru.browsers import ChromeBrowser, EdgeBrowser, ChromiumBrowser
from miru.utils.enums import BrowsersEnum
from miru.utils.dataclasses import AppConfig


config: AppConfig = app.config["miru_config"]

def init(
    web_folder: str = None,
    mode: BrowsersEnum = None,
    cmd_args: List = None,
    size: Tuple[int, int] = None,
    position: Tuple[int, int] = None,
    port: int = None
) -> None:
    """
    Initializes the web folder, browser settings and port.

    Parameters:
    - web_folder: User web folder.
    - mode: Browser mode.
    - cmd_args: Browser arguments.
    - size: Window size.
    - position: Window position.
    - port: Application port.

    Returns:
    - None.
    """
    if web_folder:
        config.user_web_dir = path.abspath(path.join(web_folder, "dist"))

    if mode:
        config.mode = mode

    if cmd_args:
        config.cmd_args = cmd_args

    if size:
        config.size = size

    if position:
        config.position = position

    if port:
        config.port = port

    if mode == BrowsersEnum.CHROME:
        browser = ChromeBrowser()

    elif mode == BrowsersEnum.CHROMIUM:
        browser = ChromiumBrowser()

    elif mode == BrowsersEnum.EDGE:
        browser = EdgeBrowser()

    else:
        raise Exception("Unknown browser mode")

    config.browser = browser

def start(app_html: str = None) -> None:
    """
    Starts the server and opens the browser with the given HTML page.

    Parameters:
    - app_html: Application html file to load in browser.

    Returns:
    - None.
    """
    if app_html:
        config.main_page = app_html

    app.merge(routes_router)
    app.merge(websockets_router)

    def open_browser_when_ready():
        if wait_for_server(config.port):
            config.browser.launch(
                page="",
                config=config,
            )

    Timer(1, open_browser_when_ready).start()

    run(
        app,
        host=config.host,
        port=config.port,
        quiet=True,
        server=GeventWebSocketServer
    )
