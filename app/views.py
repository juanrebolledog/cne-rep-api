from flask import Response, request
from app.models import Voter, Center
import ujson as json
import logging
from werkzeug.contrib.cache import RedisCache
import hashlib
from sqlalchemy import asc, desc, extract, func
import datetime
import os
from libs.log_handler import CustomFileHandler
from app import api


cache = RedisCache()


@api.route('/voter/<int:idnum>')
def search_voter(idnum):
    voter = Voter.query.filter_by(document_id=idnum).first()
    if voter:
        voter = voter.todict()
    else:
        voter = {}
    return Response(json.dumps(voter), mimetype='application/json')


@api.route('/voters/<int:centerid>')
def search_voters_center(centerid):
    voters = cache.get('voters-center-' + str(centerid))
    if voters is None:
        voters = Voter.query.filter_by(center_code=centerid).all()
        voters = map(Voter.todict, voters)
        cache.set('voters-center-' + str(centerid), voters, timeout=5 * 60)
    return Response(json.dumps(voters), mimetype='application/json')


@api.route('/voters/<int:centerid>/age/<string:calc_type>')
def search_voters_center_age(centerid, calc_type):
    calc_types = ['min', 'max', 'avg', 'dist']
    calc_type = calc_type.lower()
    if calc_type in calc_types:
        cache_name = 'voters-center-age-' \
                     + str(calc_type) + '-' + str(centerid)
        voters = cache.get(cache_name)

        if voters is None:
            def age(dob):
                today = datetime.date.today()
                if today.month < dob.month or \
                        (today.month == dob.month and today.day < dob.day):
                    return today.year - dob.year - 1
                else:
                    return today.year - dob.year

            if calc_type == 'max':
                voter = Voter.query.filter_by(center_code=centerid).\
                    order_by(asc(Voter.birth_date)).first()
                voter_dict = voter.todict()
                result = {
                    'center_code': centerid,
                    'birth_date': voter.birth_date.strftime('%Y-%m-%d'),
                    'age': age(voter.birth_date),
                    'voter': voter_dict
                }

            if calc_type == 'min':
                voter = Voter.query.filter_by(center_code=centerid).\
                    order_by(desc(Voter.birth_date)).first()
                voter_dict = voter.todict()
                result = {
                    'center_code': centerid,
                    'birth_date': voter.birth_date.strftime('%Y-%m-%d'),
                    'age': age(voter.birth_date),
                    'voter': voter_dict
                }

            if calc_type == 'avg':
                distribution = Voter.query.\
                    with_entities(extract('year', datetime.date.today()) -
                                  extract('year', Voter.birth_date),
                                  func.count(Voter.birth_date)).\
                    filter_by(center_code=centerid).\
                    group_by(extract('year', Voter.birth_date)).\
                    order_by(desc(Voter.birth_date)).all()
                voter_dist = map(
                    lambda tuple: {'age': tuple[0], 'count': tuple[1]},
                    distribution)
                total = 0
                avg = 0
                for group in voter_dist:
                    total += group['count']
                    avg += group['age'] * group['count']

                avg = float(avg)/float(total)
                result = {
                    'center_code': centerid,
                    'avg': avg
                }

            if calc_type == 'dist':
                distribution = Voter.query.\
                    with_entities(extract('year', datetime.date.today()) -
                                  extract('year', Voter.birth_date),
                                  func.count(Voter.birth_date)).\
                    filter_by(center_code=centerid).\
                    group_by(extract('year', Voter.birth_date)).\
                    order_by(desc(Voter.birth_date)).all()
                voter_dist = map(
                    lambda tuple: {'age': tuple[0], 'count': tuple[1]},
                    distribution)
                result = {
                    'center_code': centerid,
                    'dist': voter_dist
                }

            cache.set('voters-center-age-' + str(type) + '-' + str(centerid),
                      voters, timeout=5 * 60)
    return Response(json.dumps(result), mimetype='application/json')


@api.route('/center/<int:centerid>')
def search_center(centerid):
    center = Center.query.filter_by(code=centerid).first()
    return Response(json.dumps(center.todict()), mimetype='application/json')


@api.route('/centers')
def search_centers_filter():
    args = {
        'state_code': request.args.get('state', ''),
        'municipality_code': request.args.get('municipality', ''),
        'parish_code': request.args.get('parish', '')
    }
    filter_hash = hashlib.\
        sha1(args['state_code'] +
             args['municipality_code'] +
             args['parish_code']).\
        hexdigest()
    for i in args.keys():
        if args[i] == '':
            del args[i]

    centers = cache.get('centers-filter-' + str(filter_hash))
    if centers is None:
        centers = Center.query.filter_by(**args).all()
        centers = map(Center.todict, centers)
        cache.set('centers-filter-' +
                  str(filter_hash),
                  centers,
                  timeout=5 * 60)
    return Response(json.dumps(centers), mimetype='application/json')
