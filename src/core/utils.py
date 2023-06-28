import time
from typing import Any, Dict, Union

from dotenv import dotenv_values


__ENV_VALUES = None
__APP_ALIVE = True


def current_time() -> int:
    return int(time.time() * 1000)


def get_env_values(key: str = None) -> Union[str, Dict[str, str]]:
    if __ENV_VALUES is None:
        set_env_values(dotenv_values(".env"))
    if key is None:
        return __ENV_VALUES
    else:
        return __ENV_VALUES[key]

def set_env_value(key: str, value: Any) -> None:
    global __ENV_VALUES
    __ENV_VALUES[key] = value

def set_env_values(values: Dict[str, Any]) -> None:
    global __ENV_VALUES
    __ENV_VALUES = values


def is_app_alive() -> bool:
    return __APP_ALIVE


def set_app_alive(value: bool):
    global __APP_ALIVE
    __APP_ALIVE = False

def from_rgb(R: int, G: int, B: int):
    return "#%02x%02x%02x" % (R, G, B)  