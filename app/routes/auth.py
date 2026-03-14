from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/landing")
def landing():
    return render_template("landing.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    conn = get_db()
    cursor = conn.cursor()

    sellers = cursor.execute(
        "SELECT uid, company FROM users WHERE role = 'seller'"
    ).fetchall()
    buyers = cursor.execute(
        "SELECT uid, company FROM users WHERE role = 'buyer'"
    ).fetchall()

    if request.method == "POST":
        uid = request.form.get("uid", "").strip()

        if not uid:
            flash("Please select an account.", "warning")
            return redirect(url_for("auth.login"))

        user = cursor.execute(
            "SELECT * FROM users WHERE uid = ?", (uid,)
        ).fetchone()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("auth.login"))

        session["uid"] = user["uid"]
        session["company"] = user["company"]
        session["role"] = user["role"]

        if user["role"] == "seller":
            return redirect(url_for("seller.dashboard"))
        else:
            return redirect(url_for("buyer.dashboard"))

    return render_template("login.html", sellers=sellers, buyers=buyers)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.landing"))