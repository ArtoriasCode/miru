from os import path
from typing import Union

from bottle import static_file, response, Bottle

from miru.misc import app
from miru.utils.dataclasses import AppConfig


router = Bottle()
config: AppConfig = app.config["miru_config"]

@router.route("/miru.js")
def serve_miru_js() -> None:
    """
    Returns the miru.js script.

    Parameters:
    - None.

    Returns:
    - None.
    """
    return static_file("miru.js", root=config.app_web_dir, mimetype="application/javascript")

@router.route("/<filepath:path>")
def serve_user_files(filepath: path) -> Union[str, None]:
    """
    Returns the user custom files.

    Parameters:
    - None.

    Returns:
    - None.
    """
    if not config.user_web_dir:
        response.status = 404
        return "User folder not set"

    return static_file(filepath, root=config.user_web_dir)

@app.route('/')
def index() -> None:
    """
    Returns the application main page.

    Parameters:
    - None.

    Returns:
    - None.
    """
    return static_file(config.main_page, root=config.user_web_dir)
