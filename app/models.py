from app import db


class Voter(db.Model):

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
    state_code = db.Column(db.Integer)
    municipality_code = db.Column(db.Integer)
    parish_code = db.Column(db.Integer)
    center_code = db.Column(db.Integer)

    def __repr__(self):
        return '<Voter "{}-{}">'.format(self.nationality, self.document_id)

    def todict(self):
        return {
            'nationality': self.nationality,
            'document_id': self.document_id,
            'first_last_name': self.first_last_name,
            'second_last_name': self.second_last_name,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'birth_date': self.birth_date.strftime('%Y-%m-%d'),
            'gender': self.gender,
            'state_code': self.state_code,
            'municipality_code': self.municipality_code,
            'parish_code': self.parish_code,
            'center_code': self.center_code
        }


class Center(db.Model):

    __tablename__ = 'voting_centers'

    id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.Integer)
    municipality_code = db.Column(db.Integer)
    parish_code = db.Column(db.Integer)
    code = db.Column(db.Integer)
    name = db.Column(db.String(200))
    address = db.Column(db.String(300))

    def __repr__(self):
        return '<Center "{}-{}">'.format(self.center_code, self.name)

    def todict(self):
        return {
            'state_code': self.state_code,
            'municipality_code': self.municipality_code,
            'parish_code': self.parish_code,
            'code': self.code,
            'name': self.name,
            'address': self.address
        }
