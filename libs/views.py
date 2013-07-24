from libs import app
from flask import Response, request
from libs.models import Voter, Center
import json
import logging
from werkzeug.contrib.cache import RedisCache
import hashlib


cache = RedisCache()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@app.route('/voter/<int:idnum>')
def search_voter(idnum):
    voter = Voter.query.filter_by(document_id=idnum).first()
    return Response(json.dumps(voter.todict()), mimetype='application/json')

@app.route('/voters/<int:centerid>')
def search_voters_center(centerid):
    voters = cache.get('voters-center-' + str(centerid))
    if voters is None:
        voters = Voter.query.filter_by(center_code=centerid).all()
        voters = map(Voter.todict, voters)
        cache.set('voters-center-' + str(centerid), voters, timeout=5 * 60)
    return Response(json.dumps(voters), mimetype='application/json')

@app.route('/center/<int:centerid>')
def search_center(centerid):
    center = Center.query.filter_by(code=centerid).first()
    return Response(json.dumps(center.todict()), mimetype='application/json')

@app.route('/centers')
def search_centers_filter():
    args = {
        'state_code': request.args.get('state', ''),
        'municipality_code': request.args.get('municipality', ''),
        'parish_code': request.args.get('parish', '')
    }
    filter_hash = hashlib.sha1(args['state_code'] + args['municipality_code'] + args['parish_code']).hexdigest()
    for i in args.keys():
        if args[i] == '':
            del args[i]

    centers = cache.get('centers-filter-' + str(filter_hash))
    if centers is None:
        centers = Center.query.filter_by(**args).all()
        centers = map(Center.todict, centers)
        cache.set('centers-filter-' + str(filter_hash), centers, timeout=5 * 60)
    return Response(json.dumps(centers), mimetype='application/json')
