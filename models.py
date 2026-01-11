from datetime import datetime
from extensions import db

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text)
    cijena = db.Column(db.Float)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(150), nullable=False)
    opis = db.Column(db.Text)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    poruka = db.Column(db.String(500), nullable=False)

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    event_naziv = db.Column(db.String(150), nullable=False)
    poruka = db.Column(db.Text)
    datum_prijave = db.Column(db.DateTime, default=datetime.utcnow)
