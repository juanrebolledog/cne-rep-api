import os
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import config

api = Flask(__name__)
api.config.from_object(config)
db = SQLAlchemy(api)

from app import views, models
from libs.log_handler import CustomFileHandler


db_logger = logging.getLogger('sqlalchemy.engine')
db_logger.setLevel(logging.INFO)
handler = CustomFileHandler(
    os.path.join(os.path.dirname(__file__), 'logs'),
    db_logger, logging.FileHandler)
db_logger.addHandler(handler)

api.logger.setLevel(logging.INFO)
handler = CustomFileHandler(
    os.path.join(os.path.dirname(__file__), 'logs'),
    api.logger, logging.FileHandler)
api.logger.addHandler(handler)
