from dataclasses import dataclass
from typing import List, Tuple, Dict, Set

from miru.utils.enums import BrowsersEnum


@dataclass
class AppConfig:
    host: str
    port: int
    mode: BrowsersEnum
    cmd_args: List[str]
    window_size: Tuple[int, int]
    window_position: Tuple[int, int]
    main_page: str
    browser: object
    user_web_dir: str
    app_web_dir: str
    listened_functions: Dict
    ws_clients: Set
