# utils.py
import os
import shutil
from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for, flash
from models import User
from extensions import db

def auto_backup():
    """
    Automatski pravi lokalnu kopiju baze (za razvoj i testiranje).
    Na produkciji (Render) može se proširiti da šalje kopiju u Google Drive.
    """
    try:
        # Kreiraj direktorij za backup ako ne postoji
        backup_dir = os.path.join(os.path.dirname(__file__), "backup")
        os.makedirs(backup_dir, exist_ok=True)

        # Naziv backup datoteke
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"versus_auto_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)

        # Glavna baza
        db_path = os.path.join(os.path.dirname(__file__), "versus.db")

        # Kopiraj bazu
        if os.path.exists(db_path):
            shutil.copy(db_path, backup_path)
            print(f"✅ Backup kreiran: {backup_filename}")
        else:
            print("⚠️ Baza nije pronađena!")

    except Exception as e:
        print(f"⚠️ Greška u backupu: {e}")

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id)

        if not user or user.role != "admin":
            flash("Nemate pristup ovoj stranici.", "warning")
            return redirect(url_for("auth.admin_login"))

        return f(*args, **kwargs)

    return wrapper