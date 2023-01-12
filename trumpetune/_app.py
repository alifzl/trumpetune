from gevent import monkey

monkey.patch_all()
import gevent
import gevent.pool
import os
import sys
import glob
import time
import uuid
import ujson
import falcon
import mimetypes
from functools import partial

from . import _utils

class Meta(object):
    def on_get(self, req, resp):
        if req.params.get("example") == "true":
            resp.content_type = mimetypes.guess_type(_utils.example[0])[0]
            resp.stream = open(_utils.example[0], "rb")
            resp.downloadable_as = os.path.basename(_utils.example[0])

        else:
            ALL_META = {}
            for k, v in _utils.META_INDEX.items():
                ALL_META[k] = v

            ALL_META["is_file_input"] = IS_FILE_INPUT
            ALL_META["example"] = _utils.example

            resp.media = ALL_META
            resp.status = falcon.HTTP_200


class Res(object):
    def on_post(self, req, resp):
        try:
            unique_id = req.media["unique_id"]
            _utils.logger.info(f"unique_id: {unique_id} Result request received.")
            try:
                pred = RESULTS_INDEX.pop(unique_id)
                resp.media = {"success": True, "prediction": pred}
                _metrics = _utils.METRICS_INDEX[unique_id]
                _metrics["responded"] = time.time()
                _utils.METRICS_INDEX[unique_id] = _metrics
            except:
                if unique_id in REQUEST_INDEX:
                    resp.media = {"success": None, "reason": "processing"}
                else:
                    resp.media = {
                        "success": False,
                        "reason": "No request found with this unique_id",
                    }

            resp.status = falcon.HTTP_200

        except Exception as ex:
            _utils.logger.exception(ex, exc_info=True)
            resp.media = {"success": False, "reason": str(ex)}
            resp.status = falcon.HTTP_400


json_handler = falcon.media.JSONHandler(
    loads=ujson.loads, dumps=partial(ujson.dumps, ensure_ascii=False)
)

extra_handlers = {
    "application/json": json_handler,
}

app = falcon.App(cors_enable=True)
app.req_options.media_handlers.update(extra_handlers)
app.resp_options.media_handlers.update(extra_handlers)
app.req_options.auto_parse_form_urlencoded = True
app = falcon.App(
    middleware=falcon.CORSMiddleware(
        allow_origins=_utils.ALLOWED_ORIGINS, allow_credentials=_utils.ALLOWED_ORIGINS
    )
)


app.add_static_route(
    "/",
    _utils.TRUMPETUNE_UI_PATH,
    fallback_filename="index.html",
)


def websocket_handler(env, start_response):
    if "wsgi.websocket" in env:
        ws = env["wsgi.websocket"]

        connection_id = f"{uuid.uuid4()}"
        n = 0
        start_time = time.time()
        _utils.logger.info(f"{self.connection_id} websocket connection opened.")

        while True:
            msg = ws.receive()
            if msg is None:
                break

            message_id = f"{connection_id}.{n}"
            REQUEST_INDEX[message_id] = [message]
            preds, status = wait_and_read_pred(message_id)
            if "prediction" in preds:
                preds["prediction"] = preds["prediction"][0]

            ws.send(ujson.dumps(preds))

        _utils.logger.info(
            f"{self.connection_id} websocket connection closed. Time spent: {time.time() - self.start_time} n_mesages: {self.n}"
        )
