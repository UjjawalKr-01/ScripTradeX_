from flask import Blueprint, redirect, url_for, session, flash, render_template, request
from app.utils import login_required
from app.services.escrow import (initiate_escrow, seller_confirm,
                                  buyer_final_confirm, settle, cancel_escrow)
from app.db import get_db

escrow_bp = Blueprint("escrow", __name__, url_prefix="/escrow")

@escrow_bp.route("/initiate/<listing_id>", methods=["POST"])
@login_required(role="buyer")
def initiate(listing_id):
    result = initiate_escrow(listing_id, session["uid"])
    if result["success"]:
        flash("✅ Scrip locked. Seller has been notified.", "success")
    else:
        flash(result["message"], "danger")
    return redirect(url_for("buyer.dashboard"))

@escrow_bp.route("/seller-confirm/<txn_id>", methods=["POST"])
@login_required(role="seller")
def confirm(txn_id):
    result = seller_confirm(txn_id, session["uid"])
    if result["success"]:
        flash("✅ Confirmed. Buyer will now proceed to payment.", "success")
    else:
        flash(result["message"], "danger")
    return redirect(url_for("seller.dashboard"))

@escrow_bp.route("/payment/<txn_id>")
@login_required(role="buyer")
def payment(txn_id):
    conn = get_db()
    cursor = conn.cursor()
    txn = cursor.execute(
        """SELECT * FROM transactions
           WHERE txnId = ? AND buyerId = ? AND escrowStatus = 'SELLER_CONFIRMED'""",
        (txn_id, session["uid"])
    ).fetchone()
    if not txn:
        flash("Payment not available for this transaction.", "danger")
        return redirect(url_for("buyer.dashboard"))
    return render_template("payment.html", txn=dict(txn))

@escrow_bp.route("/payment/<txn_id>/process", methods=["POST"])
@login_required(role="buyer")
def process_payment(txn_id):
    name        = request.form.get("name", "").strip()
    card_number = request.form.get("card_number", "").strip()
    expiry      = request.form.get("expiry", "").strip()
    cvv         = request.form.get("cvv", "").strip()

    if not all([name, card_number, expiry, cvv]):
        flash("Please fill in all payment details.", "warning")
        return redirect(url_for("escrow.payment", txn_id=txn_id))

    result = buyer_final_confirm(txn_id, session["uid"])
    if result["success"]:
        flash("✅ Payment successful. Funds held in escrow.", "success")
        return redirect(url_for("escrow.status", txn_id=txn_id))
    else:
        flash(result["message"], "danger")
        return redirect(url_for("escrow.payment", txn_id=txn_id))

@escrow_bp.route("/settle/<txn_id>", methods=["POST"])
@login_required(role="seller")
def settle_txn(txn_id):
    result = settle(txn_id)
    if result["success"]:
        flash(f"✅ Settled. ₹{result['sellerPayout']:,.0f} credited to your account.", "success")
        if result["fineResult"]["fined"]:
            flash(
                f"⚠️ Buyer fined ₹{result['fineResult']['fineAmount']:,.0f} — {result['fineResult']['fineReason']}",
                "warning"
            )
    else:
        flash(result["message"], "danger")
    return redirect(url_for("seller.dashboard"))

@escrow_bp.route("/cancel/<txn_id>", methods=["POST"])
@login_required()
def cancel(txn_id):
    result = cancel_escrow(txn_id, session["uid"])
    if result["success"]:
        flash("Transaction cancelled. Scrip relisted.", "info")
    else:
        flash(result["message"], "danger")
    if session["role"] == "seller":
        return redirect(url_for("seller.dashboard"))
    return redirect(url_for("buyer.dashboard"))

@escrow_bp.route("/status/<txn_id>")
@login_required()
def status(txn_id):
    conn = get_db()
    cursor = conn.cursor()
    txn = cursor.execute(
        "SELECT * FROM transactions WHERE txnId = ?", (txn_id,)
    ).fetchone()
    if not txn:
        flash("Transaction not found.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("escrow_status.html", txn=dict(txn))