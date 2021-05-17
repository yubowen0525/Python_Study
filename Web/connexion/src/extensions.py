from socket import gethostname
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from loguru import logger

db = SQLAlchemy()
ma = Marshmallow()
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

logging = logger.bind(
    componentName="Controller Python Study",
    serviceName="szn",
    hostName=gethostname(),
    type="trace",
)