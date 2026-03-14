from app.db import get_db
from app.services.commission import calculate_commission
from app.services.fine import check_and_apply_fine
from datetime import datetime
import uuid

def initiate_escrow(listing_id: str, buyer_id: str) -> dict:
    conn = get_db()
    cursor = conn.cursor()

    listing = cursor.execute(
        "SELECT * FROM listings WHERE listingId = ? AND status = 'active'", (listing_id,)
    ).fetchone()
    if not listing:
        return {"success": False, "message": "Listing not available or already locked."}

    listing = dict(listing)
    txn_id = "TXN-" + str(uuid.uuid4())[:8].upper()
    commission = calculate_commission(listing["askPrice"])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """INSERT INTO transactions
           (txnId, listingId, scripId, buyerId, sellerId,
            faceValue, agreedPrice, commission, escrowStatus, createdAt)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'BUYER_INTERESTED', ?)""",
        (txn_id, listing_id, listing["scripId"], buyer_id,
         listing["sellerId"], listing["faceValue"],
         listing["askPrice"], commission, now)
    )
    cursor.execute(
        "UPDATE listings SET status = 'locked', lockedByBuyerId = ? WHERE listingId = ?",
        (buyer_id, listing_id)
    )
    cursor.execute(
        "UPDATE gov_registry SET status = 'in_escrow' WHERE scripId = ?",
        (listing["scripId"],)
    )
    cursor.execute(
        """INSERT INTO notifications (uid, message, type, read, createdAt)
           VALUES (?, ?, 'scrip_interest', 0, ?)""",
        (listing["sellerId"],
         f"A buyer has locked scrip {listing['scripId']}. Please confirm or reject.",
         now)
    )
    conn.commit()
    return {"success": True, "txnId": txn_id}

def seller_confirm(txn_id: str, seller_id: str) -> dict:
    conn = get_db()
    cursor = conn.cursor()

    txn = cursor.execute(
        """SELECT * FROM transactions
           WHERE txnId = ? AND sellerId = ? AND escrowStatus = 'BUYER_INTERESTED'""",
        (txn_id, seller_id)
    ).fetchone()
    if not txn:
        return {"success": False, "message": "Transaction not found or already actioned."}

    cursor.execute(
        "UPDATE transactions SET escrowStatus = 'SELLER_CONFIRMED' WHERE txnId = ?",
        (txn_id,)
    )
    cursor.execute(
        """INSERT INTO notifications (uid, message, type, read, createdAt)
           VALUES (?, ?, 'locked', 0, ?)""",
        (dict(txn)["buyerId"],
         f"Seller confirmed transaction {txn_id}. Please proceed to payment.",
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    return {"success": True}

def buyer_final_confirm(txn_id: str, buyer_id: str) -> dict:
    conn = get_db()
    cursor = conn.cursor()

    txn = cursor.execute(
        """SELECT * FROM transactions
           WHERE txnId = ? AND buyerId = ? AND escrowStatus = 'SELLER_CONFIRMED'""",
        (txn_id, buyer_id)
    ).fetchone()
    if not txn:
        return {"success": False, "message": "Transaction not ready for payment."}

    txn = dict(txn)
    buyer = dict(cursor.execute(
        "SELECT * FROM users WHERE uid = ?", (buyer_id,)
    ).fetchone())

    if buyer["balance"] < txn["agreedPrice"]:
        return {"success": False, "message": "Insufficient wallet balance."}

    cursor.execute(
        "UPDATE users SET balance = balance - ? WHERE uid = ?",
        (txn["agreedPrice"], buyer_id)
    )
    cursor.execute(
        "UPDATE transactions SET escrowStatus = 'FUNDS_HELD' WHERE txnId = ?",
        (txn_id,)
    )
    conn.commit()
    return {"success": True}

def settle(txn_id: str) -> dict:
    conn = get_db()
    cursor = conn.cursor()

    txn = cursor.execute(
        "SELECT * FROM transactions WHERE txnId = ? AND escrowStatus = 'FUNDS_HELD'",
        (txn_id,)
    ).fetchone()
    if not txn:
        return {"success": False, "message": "Transaction not ready for settlement."}

    txn = dict(txn)

    # Check and apply fine before settling
    fine_result = check_and_apply_fine(txn_id)

    seller_payout = txn["agreedPrice"] - txn["commission"]

    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE uid = ?",
        (seller_payout, txn["sellerId"])
    )
    cursor.execute(
        "UPDATE gov_registry SET currentOwnerUid = ?, status = 'transferred' WHERE scripId = ?",
        (txn["buyerId"], txn["scripId"])
    )
    cursor.execute(
        "UPDATE transactions SET escrowStatus = 'SETTLED' WHERE txnId = ?", (txn_id,)
    )
    cursor.execute(
        "UPDATE listings SET status = 'sold' WHERE listingId = ?", (txn["listingId"],)
    )
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Notify seller
    cursor.execute(
        """INSERT INTO notifications (uid, message, type, read, createdAt)
           VALUES (?, ?, 'settled', 0, ?)""",
        (txn["sellerId"],
         f"Transaction {txn_id} settled. ₹{seller_payout:,.0f} credited.",
         now)
    )

    # Notify buyer — include fine info if applicable
    buyer_msg = f"Transaction {txn_id} complete. Scrip {txn['scripId']} transferred to you."
    if fine_result["fined"]:
        buyer_msg += f" Note: ₹{fine_result['fineAmount']:,.0f} fine deducted — {fine_result['fineReason']}"

    cursor.execute(
        """INSERT INTO notifications (uid, message, type, read, createdAt)
           VALUES (?, ?, 'settled', 0, ?)""",
        (txn["buyerId"], buyer_msg, now)
    )

    conn.commit()
    return {
        "success": True,
        "sellerPayout": seller_payout,
        "fineResult": fine_result
    }
def cancel_escrow(txn_id: str, actor_id: str) -> dict:
    conn = get_db()
    cursor = conn.cursor()

    txn = cursor.execute(
        "SELECT * FROM transactions WHERE txnId = ?", (txn_id,)
    ).fetchone()
    if not txn:
        return {"success": False, "message": "Transaction not found."}

    txn = dict(txn)

    # Refund buyer if funds were already held
    if txn["escrowStatus"] == "FUNDS_HELD":
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE uid = ?",
            (txn["agreedPrice"], txn["buyerId"])
        )

    cursor.execute(
        "UPDATE transactions SET escrowStatus = 'CANCELLED', cancelledBy = ? WHERE txnId = ?",
        (actor_id, txn_id)
    )
    cursor.execute(
        "UPDATE listings SET status = 'active', lockedByBuyerId = NULL WHERE listingId = ?",
        (txn["listingId"],)
    )
    cursor.execute(
        "UPDATE gov_registry SET status = 'listed' WHERE scripId = ?", (txn["scripId"],)
    )
    conn.commit()
    return {"success": True}