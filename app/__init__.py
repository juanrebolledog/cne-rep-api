from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


from app import views, models

if not app.debug:
    import os
    import logging

    from libs.log_handler import CustomFileHandler
    from app import app

    app.logger.setLevel(logging.INFO)
    handler = CustomFileHandler(
        os.path.join(os.path.dirname(__file__), 'logs'),
        app.logger, logging.FileHandler)
    app.logger.addHandler(handler)
