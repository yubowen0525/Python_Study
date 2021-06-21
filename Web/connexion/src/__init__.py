# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       ybw
   date：          2021/3/27
-------------------------------------------------
   Change Activity:
                   2021/3/27:
-------------------------------------------------
"""
import click
from loguru import logger

from src.extensions import db, ma
from src.fakes import fake_user
from src.config.settings import config
import os
import json
import sys
from src.routes import *
import connexion
from connexion.resolver import MethodViewResolver


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    connexion_app = connexion.FlaskApp(__name__, specification_dir="./swagger/", debug=True)
    connexion_app.add_api(
        "swagger.yaml",
        arguments={"title": "Hello World Example"},
        resolver=MethodViewResolver("src.routes"),
        strict_validation=True,
        validate_responses=True,
    )
    app = connexion_app.app
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_errorhandlers(app)
    register_commands(app)
    register_logging(app)
    return app


def register_extensions(app):
    db.init_app(app)
    # api.init_app(app, add_specs=app.config["SPECS"])
    ma.init_app(app)


def register_errorhandlers(app):
    @app.errorhandler(404)
    def handle_app_exception(error):
        notfound = NotFound()
        response = jsonify(notfound.to_dict())
        response.status_code = notfound.status_code
        return response

    @app.errorhandler(RestError)
    def handle_app_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


def register_commands(app):
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop.")
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                "This operation will delete the database, do you want to continue?",
                abort=True,
            )
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    @click.option("--user", default=10, help="Quantity of users, default is 10.")
    def forge(user):
        click.echo("Generating %d users..." % user)
        fake_user(user)


# def register_request_handlers(app):
#     @app.after_request
#     def query_profiler(response):
#         for q in get_debug_queries():
#             if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
#                 app.logger.warning(
#                     'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
#                     % (q.duration, q.context, q.statement)
#                 )
#         return response


def register_logging(app):
    def customized_serializer(message):
        """Customized the fields we need."""
        record = message.record

        fields = {
            "level": record["level"].name,
            "message": dict(detail=record["message"]),
            "timestamp": record["time"].isoformat(),
            "traceId": record["extra"].get("traceId", str(uuid.uuid4())),
            "taskId": record["extra"].get("taskId", str(uuid.uuid4())),
            "type": "trace",
            "serviceName": "szn",
            "componentName": "Controller SASEOne Proxy",
        }

        if "traceId" in record["extra"]:
            del record["extra"]["traceId"]

        if "taskId" in record["extra"]:
            del record["extra"]["taskId"]

        if record["exception"]:
            fields["message"]["exception"] = "".join(
                traceback.format_exception(
                    type(record["exception"].value),
                    record["exception"].value,
                    record["exception"].traceback,
                )
            )
        # Gather the bidning fields
        fields["message"].update(record["extra"])
        fileds = json.dumps(fields)
        print(fileds, file=sys.stdout)

    logger.remove(handler_id=None)
    # logger.add(sys.stderr, level=app.config["LOG_LEVEL"])
    logger.add(customized_serializer, level=app.config["LOG_LEVEL"])
