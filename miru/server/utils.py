import os
from json import dumps
from time import time, sleep
from socket import socket
from typing import Callable

from miru.misc import app
from miru.utils.dataclasses import AppConfig


config: AppConfig = app.config["miru_config"]

def stop_server() -> None:
    """
    Stops the server.

    Parameters:
    - None.

    Returns:
    - None.
    """
    if not config.ws_clients:
        print("No connected clients. Stopping server.")
        os._exit(0)

def call_js(function_name: str, *args) -> None:
    """
    Calls the given function with the given arguments in JavaScript.

    Parameters:
    - function_name: Function to call.
    - *args: Additional arguments to pass to the function.

    Returns:
    - None.
    """
    message = dumps({
        "type": "call",
        "name": function_name,
        "args": args
    })

    for client in list(config.ws_clients):
        try:
            client.send(message)
        except:
            config.ws_clients.discard(client)

def listen(func: Callable) -> Callable:
    """
    Adds a function to the listened functions dictionary.

    Parameters:
    - func: Function to listen.

    Returns:
    - Callable: Called function.
    """
    config.listened_functions[func.__name__] = func
    return func

def wait_for_server(port: int, timeout: float = 60.0) -> bool:
    """
    Waits for the server to start up.

    Parameters:
    - port: Server port.
    - timeout: Timeout to wait for.

    Returns:
    - bool: Server is running.
    """
    start = time()

    while time() - start < timeout:
        with socket() as s:
            try:
                s.connect(("localhost", port))
                return True
            except:
                sleep(0.1)

    return False
