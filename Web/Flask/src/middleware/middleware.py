import logging
from werkzeug.wrappers import Request, Response
from src.extensions import logging
from werkzeug.local import get_ident
import urllib.parse


class middleware:
    """
    Simple WSGI middleware
    """

    def __init__(self, app):
        self.app = app
        self.point = "ns1, ns2"

    def __call__(self, environ, start_response):
        request = Request(environ)
        path = urllib.parse.urlsplit(request.url).path.split("/")[1]
        if path not in self.point or path == "":
            return self.app(environ, start_response)
        header = request.headers
        customer = header.get("x-customer-id", None)
        connector = header.get("x-connector-id", None)
        traceid = header.get("x-trace-id", None)
        if traceid is None:
            traceid = header.get("X-Appgw-Trace-Id", None)
        taskid = header.get("x-task-id", None)

        with logging.contextualize(
            companyId=customer,
            connectorId=connector,
            traceId=traceid,
            taskId=taskid,
            url=request.url,
            method=request.method,
            id=str(get_ident()),
        ):
            logging.info("start request")
            try:
                return self.app(environ, start_response)
            finally:
                logging.info("end request")
        # res = Response(u"Authorization failed", mimetype="text/plain", status=401)
        # return res(environ, start_response)