import os
import sys
import glob
import subprocess

RECIPE = os.getenv("RECIPE")
MODE = os.getenv("MODE")

if os.path.exists(RECIPE):
    sys.path.append(RECIPE)
    os.chdir(RECIPE)


def websocket():
    from ._app import websocket_handler
    from ._ws import WebSocketHandler
    from gevent.pywsgi import WSGIServer

    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")

    server = WSGIServer((host, port), websocket_handler, handler_class=WebSocketHandler)
    server.serve_forever()


if MODE == "websocket":
    websocket()
