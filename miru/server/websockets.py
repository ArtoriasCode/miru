from json import loads, dumps
from threading import Timer

from bottle import Bottle

try:
    import bottle_websocket as wbs
except ImportError:
    import bottle.ext.websocket as wbs
from bottle_websocket import websocket

from miru.misc import app
from miru.server.utils import stop_server
from miru.utils.dataclasses import AppConfig


router = Bottle()
config: AppConfig = app.config["miru_config"]

@router.route("/__miru_ws__", apply=[wbs.websocket])
def handle_ws(ws: websocket) -> None:
    """
    Listens websocket messages.

    Parameters:
    - ws: WebSocket object.

    Returns:
    - None.
    """
    config.ws_clients.add(ws)

    try:
        while True:
            msg = ws.receive()

            if msg is None:
                break

            try:
                data = loads(msg)
                msg_type = data.get("type")

                if msg_type == "call":
                    fn_name = data.get("name")
                    args = data.get("args", [])
                    kwargs = data.get("kwargs", {})
                    call_id = data.get("id")

                    if fn_name not in config.listened_functions:
                        ws.send(dumps({
                            "type": "error",
                            "id": call_id,
                            "error": f"Function '{fn_name}' not found"
                        }))

                        continue

                    try:
                        result = config.listened_functions[fn_name](*args, **kwargs)

                        ws.send(dumps({
                            "type": "result",
                            "id": call_id,
                            "result": result
                        }))
                    except Exception as e:
                        ws.send(dumps({
                            "type": "error",
                            "id": call_id,
                            "error": str(e)
                        }))
                else:
                    pass

            except Exception as e:
                print("WebSocket error:", e)

    finally:
        config.ws_clients.discard(ws)
        Timer(3, stop_server).start()
