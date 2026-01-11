from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Contact

bp = Blueprint("user", __name__)

@bp.route("/user/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "12345":
            session["logged_in"] = True
            flash("Uspješna prijava!", "success")
            return redirect(url_for("user.user_messages"))
        else:
            flash("Pogrešno korisničko ime ili lozinka!", "danger")

    return render_template("user_login.html")


@bp.route("/user/messages")
def user_messages():
    if not session.get("logged_in"):
        flash("Prijavi se za pristup svojim porukama.", "warning")
        return redirect(url_for("user.user_login"))

    sve_poruke = Contact.query.all()
    return render_template("messages.html", poruke=sve_poruke)
