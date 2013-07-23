from libs import db
from collections import OrderedDict


class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class Voter(DictSerializable, db.Model):

    __tablename__ = 'voters'

    id = db.Column(db.Integer, primary_key=True)
    nationality = db.Column(db.String(2))
    document_id = db.Column(db.String(45))
    first_last_name = db.Column(db.String(100))
    second_last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(1))
    state_code = db.Column(db.Integer(2))
    municipality_code = db.Column(db.Integer(2))
    parish_code = db.Column(db.Integer(2))
    center_code = db.Column(db.Integer(9))

    def __init__(self, nationality=None, document_id=None):
        self.nationality = nationality
        self.document_id = document_id

    def __repr__(self):
        return '<Voter "{}-{}">'.format(self.nationality, self.document_id)


class Center(db.Model):

    __tablename__ = 'voting_centers'

    id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.Integer(2))
    municipality_code = db.Column(db.Integer(2))
    parish_code = db.Column(db.Integer(2))
    center_code = db.Column(db.Integer(9))
    name = db.Column(db.String(200))
    address = db.Column(db.String(300))

    def __init__(self, center_code=None, name=None):
        self.center_code = center_code
        self.name = name

    def __repr__(self):
        return '<Center "{}-{}">'.format(self.center_code, self.name)