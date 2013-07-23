from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from libs import views, models

if not app.debug:
    import os
    import logging
    from logging import Formatter, FileHandler

    file_handler = FileHandler(os.path.join(os.path.dirname(__name__), 'error.log'))
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
'[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

