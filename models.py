from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    cijena = db.Column(db.Float)

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


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
