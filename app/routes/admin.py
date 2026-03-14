from flask import Blueprint, render_template, session, redirect, url_for
from app.db import get_db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ADMIN_KEY = "scriptradex-admin"

@admin_bp.route("/dashboard")
def dashboard():
    if session.get("admin") != ADMIN_KEY:
        return redirect(url_for("admin.login"))

    conn = get_db()
    cursor = conn.cursor()

    settled = cursor.execute(
        """SELECT t.*,
                  ub.company as buyerCompany,
                  us.company as sellerCompany
           FROM transactions t
           JOIN users ub ON t.buyerId = ub.uid
           JOIN users us ON t.sellerId = us.uid
           WHERE t.escrowStatus = 'SETTLED'
           ORDER BY t.createdAt DESC"""
    ).fetchall()
    settled = [dict(s) for s in settled]

    total_commission = sum(t["commission"] for t in settled)
    total_volume     = sum(t["agreedPrice"] for t in settled)
    total_txns       = len(settled)

    all_txns = cursor.execute(
        """SELECT t.escrowStatus, COUNT(*) as count
           FROM transactions t
           GROUP BY t.escrowStatus"""
    ).fetchall()
    all_txns = [dict(t) for t in all_txns]

    return render_template("admin_dashboard.html",
        settled=settled,
        total_commission=total_commission,
        total_volume=total_volume,
        total_txns=total_txns,
        all_txns=all_txns
    )

@admin_bp.route("/login")
def login():
    session["admin"] = ADMIN_KEY
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("auth.landing"))