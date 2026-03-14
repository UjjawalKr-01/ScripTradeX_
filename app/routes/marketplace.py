from flask import Blueprint, render_template, request, session
from app.db import get_db
from app.utils import login_required
from datetime import datetime, timedelta

marketplace_bp = Blueprint("marketplace", __name__, url_prefix="/marketplace")

@marketplace_bp.route("/")
@login_required()
def index():
    conn = get_db()
    cursor = conn.cursor()

    scrip_type      = request.args.get("type", "any")
    min_value       = request.args.get("min", 0, type=float)
    max_value       = request.args.get("max", 99999999, type=float)
    min_expiry_days = request.args.get("days", 0, type=int)
    min_expiry_date = (datetime.today() + timedelta(days=min_expiry_days)).strftime("%Y-%m-%d")

    if scrip_type and scrip_type != "any":
        listings = cursor.execute(
            """SELECT l.*, u.company as sellerCompany
               FROM listings l JOIN users u ON l.sellerId = u.uid
               WHERE l.status = 'active' AND l.type = ?
               AND l.faceValue BETWEEN ? AND ?
               AND l.expiryDate >= ?
               ORDER BY l.discountRate DESC""",
            (scrip_type, min_value, max_value, min_expiry_date)
        ).fetchall()
    else:
        listings = cursor.execute(
            """SELECT l.*, u.company as sellerCompany
               FROM listings l JOIN users u ON l.sellerId = u.uid
               WHERE l.status = 'active'
               AND l.faceValue BETWEEN ? AND ?
               AND l.expiryDate >= ?
               ORDER BY l.discountRate DESC""",
            (min_value, max_value, min_expiry_date)
        ).fetchall()

    listings = [dict(l) for l in listings]
    filters_applied = (scrip_type != "any" or min_value > 0
                       or max_value < 99999999 or min_expiry_days > 0)

    return render_template("marketplace.html",
        listings=listings,
        filters_applied=filters_applied,
        scrip_type=scrip_type,
        min_value=min_value,
        max_value=max_value,
        min_expiry_days=min_expiry_days
    )