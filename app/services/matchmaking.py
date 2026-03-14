from app.db import get_db
from datetime import datetime, timedelta

def find_matches(scrip_type: str, min_value: float,
                 max_value: float, min_expiry_days: int) -> list:
    conn = get_db()
    cursor = conn.cursor()
    min_expiry_date = (datetime.today() + timedelta(days=min_expiry_days)).strftime("%Y-%m-%d")

    if scrip_type and scrip_type != "any":
        rows = cursor.execute(
            """SELECT l.*, u.company as sellerCompany
               FROM listings l JOIN users u ON l.sellerId = u.uid
               WHERE l.status = 'active' AND l.type = ?
               AND l.faceValue BETWEEN ? AND ?
               AND l.expiryDate >= ?
               ORDER BY l.discountRate DESC""",
            (scrip_type, min_value, max_value, min_expiry_date)
        ).fetchall()
    else:
        rows = cursor.execute(
            """SELECT l.*, u.company as sellerCompany
               FROM listings l JOIN users u ON l.sellerId = u.uid
               WHERE l.status = 'active'
               AND l.faceValue BETWEEN ? AND ?
               AND l.expiryDate >= ?
               ORDER BY l.discountRate DESC""",
            (min_value, max_value, min_expiry_date)
        ).fetchall()

    return [dict(r) for r in rows]