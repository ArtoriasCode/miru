from os import path
from pathlib import Path

from bottle import Bottle

from miru.utils.enums import BrowsersEnum
from miru.utils.dataclasses import AppConfig

app = Bottle()
app.config["miru_config"]: AppConfig = AppConfig(
    host="localhost",
    port=8383,
    mode=BrowsersEnum.CHROME,
    cmd_args=["--disable-http-cache"],
    window_size=(600, 600),
    window_position=(0, 0),
    main_page="index.html",
    browser=None,
    app_web_dir=str(Path(Path(__file__).resolve().parent) / "web"),
    user_web_dir=path.abspath(path.join("frontend", "dist")),
    listened_functions={},
    ws_clients=set(),
)
