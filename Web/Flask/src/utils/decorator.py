from flask import request
from src.extensions import logging
from werkzeug.local import LocalStack, release_local, get_ident
import functools
from contextlib import contextmanager

extra_message = LocalStack()


@contextmanager
def context_message(local_context, msg):
    # add msg to local coroutine or thread
    if local_context:
        extra_message.push(msg)
    try:
        yield
    finally:
        # clear msg of local coroutine or thread
        if local_context:
            release_local(extra_message)


def add_logging_context(local_context=False):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            header = request.headers
            customer = header.get("x-customer-id", None)
            connector = header.get("x-connector-id", None)
            traceid = header.get("x-trace-id", None)
            if traceid is None:
                traceid = header.get("X-Appgw-Trace-Id", None)
            taskid = header.get("x-task-id", None)

            with context_message(
                local_context,
                dict(
                    companyId=customer,
                    connectorId=connector,
                    traceId=traceid,
                    taskId=taskid,
                ),
            ):
                with logging.contextualize(
                    companyId=customer,
                    connectorId=connector,
                    traceId=traceid,
                    taskId=taskid,
                    url=request.url,
                    method=request.method,
                    id=str(get_ident()),
                ):
                    logging.info("Start processing the request.")
                    try:
                        result = func(*args, **kwargs)
                        return result
                    finally:
                        logging.info("End of processing the request.")

        return wrapped

    return wrapper
