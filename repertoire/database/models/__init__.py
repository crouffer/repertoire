from ..flask_db import get_db

db = get_db()


class Act(db.Model):
    """
    An Act is one or more people, on one or more instruments.

    Example 1: Bob and Sally - Duet:
    - Bob (Vocals, Acoustic Guitar, Electric Guitar)
    - Sally (Vocals, Bass)

    Example 2: Bob, Solo
    - Bob (Vocals, Acoustic Guitar)
    """
    __tablename__ = "act"
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=db.func.now(), nullable=True)
    act_name = db.Column(db.String, nullable=False)
    act_person = db.relationship("ActPerson", back_populates="act")


class ActPerson(db.Model):
    """
    Junction between the person/people in an act
    """
    __tablename__ = "act_person"
    act_id = db.Column(db.Integer, db.ForeignKey('act.id'), primary_key=True)
    act = db.relationship("Act", back_populates="act_person")

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    person = db.relationship("Person", back_populates="act_person")

    db.UniqueConstraint('act_id', 'act_id', name='ActPersonUnique')


class Person(db.Model):
    """
    A Person is exactly what you'd expect
    """
    __tablename__="person"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    date_added = db.Column(db.DateTime, default=db.func.now(), nullable=True)

    act_person = db.relationship("ActPerson", back_populates="person")
