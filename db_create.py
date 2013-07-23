__author__ = 'juanrebolledo'

from config import SQLALCHEMY_DATABASE_URI
from libs import db

db.create_all()
