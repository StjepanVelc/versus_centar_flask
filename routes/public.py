from flask import Blueprint, render_template
from models import Course, Event
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from extensions import db, mail
from models import Contact
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

@bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        ime = request.form.get("ime")
        email = request.form.get("email")
        poruka = request.form.get("poruka")

        if not ime or not email or not poruka:
            flash("Sva polja su obavezna.", "danger")
            return redirect(url_for("public.contact"))

        # 1️⃣ Spremi poruku u bazu
        nova_poruka = Contact(
            ime=ime,
            email=email,
            poruka=poruka
        )
        db.session.add(nova_poruka)
        db.session.commit()

        # 2️⃣ Pošalji email adminu
        msg = Message(
            subject="📩 Nova poruka s kontakt forme",
            recipients=["versus.centar@gmail.com"],  # admin mail
            body=f"""
Nova poruka s web stranice Versus Centar

Ime: {ime}
Email: {email}

Poruka:
{poruka}
"""
        )
        mail.send(msg)

        flash("Poruka je uspješno poslana. Hvala!", "success")
        return redirect(url_for("public.contact"))

    return render_template("contact.html")
