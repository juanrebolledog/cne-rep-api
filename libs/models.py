from libs import db


def todict(self):
    def convert_date(value):
        return value.strftime("%Y-%m-%d")

    d = {}
    for c in self.__table__.columns:
        if isinstance(c.type, db.Date):
            value = convert_date(getattr(self, c.name))
        else:
            value = getattr(self, c.name)

        yield(c.name, value)


def iterfunc(self):
    """
    Returns an iterable that supports .next()
    so we can do dict(sa_instance)
    """
    return self.todict()


db.Model.todict = todict
db.Model.__iter__ = iterfunc


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
    state_code = db.Column(db.Integer(2))
    municipality_code = db.Column(db.Integer(2))
    parish_code = db.Column(db.Integer(2))
    center_code = db.Column(db.Integer(9))

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

    def __repr__(self):
        return '<Center "{}-{}">'.format(self.center_code, self.name)
