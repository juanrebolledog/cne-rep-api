__author__ = 'juanrebolledo'

DBUSER = 'rep_api'
DBPASS = 'repuserapi123'
DBHOST = '192.168.106.128'
DBNAME = 'rep'
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(DBUSER, DBPASS, DBHOST, DBNAME)
