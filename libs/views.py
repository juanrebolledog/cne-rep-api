from libs import app
from flask import Response
from libs.models import Voter, Center
import json
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@app.route('/voter/<int:idnum>')
def search_voter(idnum):
    voter = Voter.query.filter_by(document_id=idnum).first()
    return Response(json.dumps(dict(voter)), mimetype='application/json')

@app.route('/voters/<int:centerid>')
def search_voters_center(centerid):
    voters = Voter.query.filter_by(center_code=centerid).all()
    voters = map(dict, voters)
    return Response(json.dumps(voters), mimetype='application/json')

@app.route('/center/<int:centerid>')
def search_center(centerid):
    center = Center.query.filter_by(center_code=centerid).first()
    return Response(json.dumps(dict(center)), mimetype='application/json')
