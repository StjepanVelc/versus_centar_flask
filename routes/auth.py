import os
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from models import User
from extensions import db
from utils import admin_required
from models import Course, Event, Contact
from extensions import limiter

bp = Blueprint("auth", __name__)

@limiter.limit("5 per minute")
@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.role == "admin":
            session["user_id"] = user.id 
            flash("Dobrodošao nazad, admin!", "success")
            return redirect(url_for("auth.admin_dashboard"))
        else:
            flash("Neispravni podaci za prijavu.", "danger")

    return render_template("login.html")

@bp.route("/add_event", methods=["GET", "POST"])
@admin_required
def add_event():
    
    if request.method == "POST":
        naziv = request.form.get("naziv")
        opis = request.form.get("opis")

        novi_dogadjaj = Event(naziv=naziv, opis=opis)
        db.session.add(novi_dogadjaj)
        db.session.commit()

        flash("Novi događaj je uspješno dodan!", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template("add_event.html")

@bp.route("/add_course", methods=["GET", "POST"])
@admin_required
def add_course():

    if request.method == "POST":
        naziv = request.form.get("naziv")
        opis = request.form.get("opis")
        cijena = request.form.get("cijena")
        cijena = float(cijena) if cijena else None

        novi_tecaj = Course(naziv=naziv, opis=opis, cijena=cijena)
        db.session.add(novi_tecaj)
        db.session.commit()

        flash("Novi tečaj je uspješno dodan!", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template("add_course.html")

@bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    sve_tecajevi = Course.query.all()
    svi_dogadjaji = Event.query.all()
    sve_poruke = Contact.query.all()

    return render_template(
        "admin_dashboard.html",
        tecajevi=sve_tecajevi,
        dogadjaji=svi_dogadjaji,
        poruke=sve_poruke,
    )

@bp.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    flash("Odjavljeni ste.", "success")
    return redirect(url_for("auth.admin_login"))

@bp.route("/delete_course/<int:course_id>", methods=["POST"])
@admin_required
def delete_course(course_id):

    tecaj = Course.query.get_or_404(course_id)
    db.session.delete(tecaj)
    db.session.commit()

    flash("Tečaj je uspješno obrisan!", "success")
    return redirect(url_for("auth.admin_dashboard"))

@bp.route("/edit_course/<int:course_id>", methods=["GET", "POST"])
@admin_required
def edit_course(course_id): 

    tecaj = Course.query.get_or_404(course_id)

    if request.method == "POST":
        tecaj.naziv = request.form.get("naziv")
        tecaj.opis = request.form.get("opis")
        cijena = request.form.get("cijena")
        tecaj.cijena = float(cijena) if cijena else None
        db.session.commit()

        flash("Tečaj je uspješno ažuriran!", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template("edit_course.html", course=tecaj)

@bp.route("/register_event/<int:event_id>", methods=["GET", "POST"])
def register_event(event_id):

    dogadjaj = Event.query.get_or_404(event_id)

    flash(f"Uspješno ste se prijavili za događaj: {dogadjaj.naziv}", "success")
    return redirect(url_for("public.events"))

@bp.route("/admin/messages")
@admin_required
def admin_messages():
    
    sve_poruke = Contact.query.all()

    return render_template("admin_messages.html", poruke=sve_poruke)

@bp.route("/admin_backup", methods=["POST"])
@admin_required
def admin_backup():
    
    # Ovdje bi išla logika za backup baze podataka
    flash("Backup baze podataka je uspješno kreiran!", "success")
    return redirect(url_for("auth.admin_dashboard"))

@bp.route("/edit_event/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_event(id):

    event = Event.query.get_or_404(id)

    if request.method == "POST":
        event.naziv = request.form.get("naziv")
        event.opis = request.form.get("opis")
        cijena = request.form.get("cijena")
        event.cijena = float(cijena) if cijena else None    
        db.session.commit()
        flash("Događaj je ažuriran.", "success")
        return redirect(url_for("public.events"))

    return render_template("edit_event.html", event=event)

@bp.route("/delete_event/<int:id>", methods=["POST"])
@admin_required
def delete_event(id):

    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()

    flash("Događaj je obrisan.", "success")
    return redirect(url_for("auth.admin_dashboard"))

@bp.route("/admin/create-admin", methods=["POST"])
@admin_required
def create_admin():

    username = request.form.get("username")
    password = request.form.get("password")

    if User.query.filter_by(username=username).first():
        flash("Korisnik već postoji.", "warning")
        return redirect(url_for("auth.admin_dashboard"))

    if len(password) < 8:
        flash("Lozinka mora imati najmanje 8 znakova.", "warning")
        return redirect(url_for("auth.admin_dashboard"))

    new_admin = User(username=username, role="admin")
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()

    flash("Novi admin uspješno kreiran.", "success")
    return redirect(url_for("auth.admin_dashboard"))

@bp.route("/admin/change-password", methods=["GET", "POST"])
@admin_required
@limiter.limit("5 per minute")
def change_password():

    user = db.session.get(User, session.get("user_id"))

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not user.check_password(old_password):
            flash("Stara lozinka nije točna.", "danger")
            return redirect(url_for("auth.change_password"))

        if len(new_password) < 8:
            flash("Nova lozinka mora imati najmanje 8 znakova.", "warning")
            return redirect(url_for("auth.change_password"))

        if new_password != confirm_password:
            flash("Lozinke se ne podudaraju.", "warning")
            return redirect(url_for("auth.change_password"))

        user.set_password(new_password)
        db.session.commit()

        flash("Lozinka promijenjena.", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template("change_password.html")