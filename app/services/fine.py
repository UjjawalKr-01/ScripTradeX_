from app.db import get_db
from datetime import datetime

FINE_RATE_EARLY  = 0.05   # 5% if scrip expires within 30 days
FINE_RATE_LATE   = 0.10   # 10% if scrip already expired
DAYS_THRESHOLD   = 30     # days to expiry that triggers fine

def check_and_apply_fine(txn_id: str) -> dict:
    """
    Check if a FUNDS_HELD transaction deserves a fine.
    Called when seller clicks Settle.
    Returns fine details if applicable.
    """
    conn = get_db()
    cursor = conn.cursor()

    txn = cursor.execute(
        "SELECT * FROM transactions WHERE txnId = ?", (txn_id,)
    ).fetchone()
    if not txn:
        return {"fined": False}

    txn = dict(txn)

    # Only apply fine on FUNDS_HELD transactions
    if txn["escrowStatus"] != "FUNDS_HELD":
        return {"fined": False}

    # Get scrip expiry date
    scrip = cursor.execute(
        "SELECT expiryDate FROM gov_registry WHERE scripId = ?",
        (txn["scripId"],)
    ).fetchone()
    if not scrip:
        return {"fined": False}

    expiry_date = datetime.strptime(scrip["expiryDate"], "%Y-%m-%d")
    today       = datetime.today()
    days_left   = (expiry_date - today).days

    fine_amount = 0
    fine_reason = None

    if days_left < 0:
        # Scrip already expired — 10% fine
        fine_amount = round(txn["faceValue"] * FINE_RATE_LATE, 2)
        fine_reason = f"Scrip expired {abs(days_left)} days ago. 10% fine on face value applied."
    elif days_left <= DAYS_THRESHOLD:
        # Scrip about to expire — 5% fine
        fine_amount = round(txn["faceValue"] * FINE_RATE_EARLY, 2)
        fine_reason = f"Scrip expires in {days_left} days (under 30-day threshold). 5% fine on face value applied."
    else:
        return {"fined": False}

    # Save fine to transaction
    cursor.execute(
        "UPDATE transactions SET finedAmount = ?, fineReason = ? WHERE txnId = ?",
        (fine_amount, fine_reason, txn_id)
    )

    # Deduct fine from buyer's balance
    cursor.execute(
        "UPDATE users SET balance = balance - ? WHERE uid = ?",
        (fine_amount, txn["buyerId"])
    )

    conn.commit()

    return {
        "fined": True,
        "fineAmount": fine_amount,
        "fineReason": fine_reason,
        "daysLeft": days_left
    }


def get_pending_fines(buyer_id: str) -> list:
    """Get all transactions where buyer was fined."""
    conn = get_db()
    cursor = conn.cursor()
    fines = cursor.execute(
        """SELECT t.*, u.company as sellerCompany
           FROM transactions t
           JOIN users u ON t.sellerId = u.uid
           WHERE t.buyerId = ? AND t.finedAmount > 0
           ORDER BY t.createdAt DESC""",
        (buyer_id,)
    ).fetchall()
    return [dict(f) for f in fines]


def get_all_fines() -> list:
    """Get all fines for admin panel."""
    conn = get_db()
    cursor = conn.cursor()
    fines = cursor.execute(
        """SELECT t.*,
                  ub.company as buyerCompany,
                  us.company as sellerCompany
           FROM transactions t
           JOIN users ub ON t.buyerId = ub.uid
           JOIN users us ON t.sellerId = us.uid
           WHERE t.finedAmount > 0
           ORDER BY t.createdAt DESC"""
    ).fetchall()
    return [dict(f) for f in fines]