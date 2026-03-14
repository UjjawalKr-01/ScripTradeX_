from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import get_db
from app.utils import login_required
from app.services.matchmaking import find_matches
import uuid
from datetime import datetime

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")

@buyer_bp.route("/dashboard")
@login_required(role="buyer")
def dashboard():
    uid = session["uid"]
    conn = get_db()
    cursor = conn.cursor()

    buyer = dict(cursor.execute(
        "SELECT * FROM users WHERE uid = ?", (uid,)
    ).fetchone())

    demands = cursor.execute(
        "SELECT * FROM buyer_demands WHERE buyerId = ? ORDER BY createdAt DESC", (uid,)
    ).fetchall()
    demands = [dict(d) for d in demands]

    deal_activity = cursor.execute(
        """SELECT t.*, u.company as sellerCompany
           FROM transactions t
           JOIN users u ON t.sellerId = u.uid
           WHERE t.buyerId = ?
           ORDER BY t.createdAt DESC""",
        (uid,)
    ).fetchall()
    deal_activity = [dict(d) for d in deal_activity]

    matches = []
    latest_demand = None
    open_demands = [d for d in demands if d["status"] == "open"]
    if open_demands:
        latest_demand = open_demands[0]
        matches = find_matches(
            latest_demand["scripType"],
            latest_demand["minValue"],
            latest_demand["maxValue"],
            latest_demand["minExpiryDays"]
        )

    from app.services.fine import get_pending_fines
    fines = get_pending_fines(uid)

    return render_template("buyer_dashboard.html",
        buyer=buyer,
        demands=demands,
        matches=matches,
        latest_demand=latest_demand,
        deal_activity=deal_activity,
        fines=fines
    )

@buyer_bp.route("/place-demand", methods=["POST"])
@login_required(role="buyer")
def place_demand():
    uid = session["uid"]
    scrip_type      = request.form.get("scrip_type", "").strip()
    min_value       = request.form.get("min_value", "").strip()
    max_value       = request.form.get("max_value", "").strip()
    min_expiry_days = request.form.get("min_expiry_days", "").strip()

    if not all([scrip_type, min_value, max_value, min_expiry_days]):
        flash("Please fill in all fields.", "warning")
        return redirect(url_for("buyer.dashboard"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE buyer_demands SET status = 'closed' WHERE buyerId = ? AND status = 'open'",
        (uid,)
    )

    demand_id = "DEM-" + str(uuid.uuid4())[:8].upper()
    cursor.execute(
        """INSERT INTO buyer_demands
           (demandId, buyerId, scripType, minValue, maxValue, minExpiryDays, status, createdAt)
           VALUES (?, ?, ?, ?, ?, ?, 'open', ?)""",
        (demand_id, uid, scrip_type, float(min_value), float(max_value),
         int(min_expiry_days), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()

    flash("✅ Demand placed. Matching scrips shown below.", "success")
    return redirect(url_for("buyer.dashboard"))

@buyer_bp.route("/cancel-demand/<demand_id>", methods=["POST"])
@login_required(role="buyer")
def cancel_demand(demand_id):
    uid = session["uid"]
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE buyer_demands SET status = 'closed' WHERE demandId = ? AND buyerId = ?",
        (demand_id, uid)
    )
    conn.commit()
    flash("Demand cancelled.", "info")
    return redirect(url_for("buyer.dashboard"))