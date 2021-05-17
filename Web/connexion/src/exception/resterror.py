# -*- coding: utf-8 -*-
"""Error code and base exception class definition."""
import json


class RestError(Exception):
    error_code = 4350
    status_code = 500
    message = "Internal Server Error."

    def __init__(self, message=None, error_code=None, status_code=None):
        if error_code:
            self.error_code = error_code

        if status_code:
            self.status_code = status_code

        if message:
            self.message = self.message + message

    def to_dict(self, **kwargs):
        ret_msg = {"error_code": self.error_code, "message": self.message}
        ret_msg.update(kwargs)

        return ret_msg

    def __str__(self):
        return json.dumps({"error_code": self.error_code, "message": self.message})


class GetNULL(RestError):
    error_code = 4310
    status_code = 200
    message = "The ip does not match any country."


class BadRequest(RestError):
    error_code = 4300
    status_code = 400
    message = "Bad Request."


class JsonFormatError(RestError):
    error_code = 4390
    status_code = 490
    message = "DataLake Response Json Format Error."


#
#
# class JsonDecodeError(RestError):
#     error_code = 4203
#     status_code = 491
#     message = 'Json Decode Error'


class NotFound(RestError):
    error_code = 4304
    status_code = 404
    message = "URL Not Found."


class InternalError(RestError):
    error_code = 4350
    status_code = 500
    message = "Internal Server Error."


class InternalRequest(InternalError):
    error_code = 4354
    status_code = 540
    message = "Internal Request to svp or ztsa error."


class InternalRequestTimeout(InternalRequest):
    error_code = 4341
    status_code = 541
    message = "Internal Request to svp or ztsa timeout."


class InternalRequestAuthFail(InternalRequest):
    error_code = 4342
    status_code = 542
    message = "Internal Request to svp or ztsa auth failed."


class InternalRedisError(RestError):
    error_code = 4351
    status_code = 551
    message = "Redis Error."


class InternalRedisReadError(InternalRedisError):
    error_code = 4351
    status_code = 551
    message = "Insert redis error."


class InternalRedisInsertError(InternalRedisError):
    error_code = 4351
    status_code = 551
    message = "Insert redis error."
