from flask import Blueprint, render_template
from models import Course, Event

bp = Blueprint("public", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/o-nama")
def about():
    return render_template("about.html")

@bp.route("/courses")
def courses():
    return render_template("courses.html", courses=Course.query.all())

@bp.route("/events")
def events():
    return render_template("events.html", events=Event.query.all())

@bp.route("/contact")
def contact():
    return render_template("contact.html")

@bp.route("/snaga_uma")
def snaga_uma():
    return render_template("snaga_uma.html")