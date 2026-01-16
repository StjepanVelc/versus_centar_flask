import os
from flask import Blueprint, request, render_template, session, flash, redirect, url_for

bp = Blueprint("auth", __name__)

@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == os.getenv("ADMIN_USERNAME")
            and password == os.getenv("ADMIN_PASSWORD")
        ):
            session["auth.admin_logged"] = True
            flash("Dobrodošao nazad, admin!", "success")
            return redirect(url_for("auth.admin_dashboard"))  # ← blueprint-safe
        else:
            flash("Neispravni podaci za prijavu.", "danger")

    return render_template("login.html")

@bp.route("/add_event", methods=["GET", "POST"])
def add_event():
    if not session.get("auth.admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    if request.method == "POST":
        naziv = request.form.get("naziv")
        opis = request.form.get("opis")

        from extensions import db
        from models import Event

        novi_dogadjaj = Event(naziv=naziv, opis=opis)
        db.session.add(novi_dogadjaj)
        db.session.commit()

        flash("Novi događaj je uspješno dodan!", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template("auth.add_event.html")

@bp.route("/add_course", methods=["GET", "POST"])
def add_course():
    if not session.get("auth.admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    if request.method == "POST":
        naziv = request.form.get("naziv")
        opis = request.form.get("opis")

        from extensions import db
        from models import Course

        novi_tecaj = Course(naziv=naziv, opis=opis)
        db.session.add(novi_tecaj)
        db.session.commit()

        flash("Novi tečaj je uspješno dodan!", "success")
        return redirect(url_for("auth.admin.dashboard"))

    return render_template("auth.add_course.html")

@bp.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("auth.admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    from models import Course, Event, Contact
    sve_tecajevi = Course.query.all()
    svi_dogadjaji = Event.query.all()
    sve_poruke = Contact.query.all()

    return render_template(
        "auth.admin_dashboard.html",
        tecajevi=sve_tecajevi,
        dogadjaji=svi_dogadjaji,
        poruke=sve_poruke,
    )

@bp.route("/admin/logout")
def admin_logout():
    session.pop("auth.admin_logged", None)
    flash("Odjavljeni ste.", "success")
    return redirect(url_for("auth.admin_login"))

@bp.route("/delete_course/<int:course_id>")
def delete_course(course_id):
    if not session.get("auth.admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    from extensions import db
    from models import Course

    tecaj = Course.query.get_or_404(course_id)
    db.session.delete(tecaj)
    db.session.commit()

    flash("Tečaj je uspješno obrisan!", "success")
    return redirect(url_for("auth.admin_dashboard"))

@bp.route("/edit_course/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id): 
    if not session.get("admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    from extensions import db
    from models import Course

    tecaj = Course.query.get_or_404(course_id)

    if request.method == "POST":
        tecaj.naziv = request.form.get("naziv")
        tecaj.opis = request.form.get("opis")

        db.session.commit()

        flash("Tečaj je uspješno ažuriran!", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template("edit_course.html", tecaj=tecaj)

@bp.route("/register_event/<int:event_id>")
def register_event(event_id):
    from models import Event

    dogadjaj = Event.query.get_or_404(event_id)

    flash(f"Uspješno ste se prijavili za događaj: {dogadjaj.naziv}", "success")
    return redirect(url_for("public.events"))

@bp.route("/admin/messages")
def admin_messages():
    if not session.get("auth.admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    from models import Contact
    sve_poruke = Contact.query.all()

    return render_template("admin_messages.html", poruke=sve_poruke)

@bp.route("/admin_backup", methods=["POST"])
def admin_backup():
    if not session.get("auth.admin_logged"):
        flash("Prijavi se kao admin za pristup ovoj stranici.", "warning")
        return redirect(url_for("auth.admin_login"))

    # Ovdje bi išla logika za backup baze podataka
    flash("Backup baze podataka je uspješno kreiran!", "success")
    return redirect(url_for("auth.admin_dashboard"))