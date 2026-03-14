from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import get_db
from app.services.gov_registry import verify_scrip, get_seller_scrips
from app.utils import login_required
import uuid

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")

@seller_bp.route("/dashboard")
@login_required(role="seller")
def dashboard():
    uid = session["uid"]
    conn = get_db()
    cursor = conn.cursor()

    listings = cursor.execute(
        "SELECT * FROM listings WHERE sellerId = ? AND status != 'sold'", (uid,)
    ).fetchall()
    listings = [dict(l) for l in listings]

    all_scrips = get_seller_scrips(uid)

    deal_activity = cursor.execute(
        """SELECT t.*, u.company as buyerCompany
           FROM transactions t
           JOIN users u ON t.buyerId = u.uid
           WHERE t.sellerId = ?
           ORDER BY t.createdAt DESC""",
        (uid,)
    ).fetchall()
    deal_activity = [dict(d) for d in deal_activity]

    return render_template("seller_dashboard.html",
        listings=listings,
        all_scrips=all_scrips,
        deal_activity=deal_activity
    )

@seller_bp.route("/list-scrip", methods=["POST"])
@login_required(role="seller")
def list_scrip():
    uid = session["uid"]
    scrip_id = request.form.get("scrip_id", "").strip()
    ask_price = request.form.get("ask_price", "").strip()

    if not scrip_id or not ask_price:
        flash("Please provide both scrip ID and asking price.", "warning")
        return redirect(url_for("seller.dashboard"))

    result = verify_scrip(scrip_id)
    if not result["valid"]:
        flash(f"Registry: {result['message']}", "danger")
        return redirect(url_for("seller.dashboard"))

    scrip = result["scrip"]

    if scrip["currentOwnerUid"] != uid:
        flash("This scrip does not belong to your account.", "danger")
        return redirect(url_for("seller.dashboard"))

    conn = get_db()
    cursor = conn.cursor()

    existing = cursor.execute(
        "SELECT * FROM listings WHERE scripId = ? AND status = 'active'", (scrip_id,)
    ).fetchone()
    if existing:
        flash("This scrip is already listed.", "warning")
        return redirect(url_for("seller.dashboard"))

    ask_price = float(ask_price)
    face_value = scrip["faceValue"]
    discount_rate = round((1 - ask_price / face_value) * 100, 2)
    listing_id = "LST-" + str(uuid.uuid4())[:8].upper()

    cursor.execute(
        """INSERT INTO listings
           (listingId, scripId, sellerId, type, faceValue, askPrice, discountRate, expiryDate, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')""",
        (listing_id, scrip_id, uid, scrip["type"], face_value,
         ask_price, discount_rate, scrip["expiryDate"])
    )
    cursor.execute(
        "UPDATE gov_registry SET status = 'listed' WHERE scripId = ?", (scrip_id,)
    )
    conn.commit()

    flash(f"✅ Scrip {scrip_id} listed successfully.", "success")
    return redirect(url_for("seller.dashboard"))

@seller_bp.route("/delist-scrip/<scrip_id>", methods=["POST"])
@login_required(role="seller")
def delist_scrip(scrip_id):
    uid = session["uid"]
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE listings SET status = 'cancelled' WHERE scripId = ? AND sellerId = ? AND status = 'active'",
        (scrip_id, uid)
    )
    cursor.execute(
        "UPDATE gov_registry SET status = 'with_exporter' WHERE scripId = ?", (scrip_id,)
    )
    conn.commit()

    flash(f"Scrip {scrip_id} delisted.", "info")
    return redirect(url_for("seller.dashboard"))