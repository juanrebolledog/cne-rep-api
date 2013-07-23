from libs import app
from flask import Response, jsonify
from libs.models import Voter, Center
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask.ext.sqlalchemy import get_debug_queries
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


@app.route('/voter/<int:idnum>')
def search_voter(idnum):
    voter = Voter.query.filter_by(document_id=idnum).first()
    print voter
    print type(voter)
    return Response(json.dumps(voter, cls=AlchemyEncoder), mimetype='application/json')

@app.route('/voters/<int:centerid>')
def search_voters_center(centerid):
    voters = Voter.query.filter_by(center_code=centerid).all()
    return Response(json.dumps(voters, cls=AlchemyEncoder), mimetype='application/json')

@app.route('/center/<int:centerid>')
def search_center(centerid):
    center = Center.query.filter_by(center_code=centerid).first()
    return Response(json.dumps(center, cls=AlchemyEncoder), mimetype='application/json')
