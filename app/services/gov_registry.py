from app.db import get_db

def get_scrip(scrip_id):
    conn = get_db()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM gov_registry WHERE scripId = ?", (scrip_id,)
    ).fetchone()
    return dict(row) if row else None

def verify_scrip(scrip_id):
    scrip = get_scrip(scrip_id)
    if not scrip:
        return {"valid": False, "message": "Scrip not found in registry."}
    if scrip["status"] == "listed":
        return {"valid": False, "message": "Scrip is already listed for sale."}
    if scrip["status"] == "in_escrow":
        return {"valid": False, "message": "Scrip is currently in escrow."}
    if scrip["status"] == "transferred":
        return {"valid": False, "message": "Scrip has already been transferred."}
    return {"valid": True, "scrip": scrip}

def get_seller_scrips(uid):
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM gov_registry WHERE currentOwnerUid = ?", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]

def transfer_scrip(scrip_id, new_owner_uid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE gov_registry SET currentOwnerUid = ?, status = 'transferred' WHERE scripId = ?",
        (new_owner_uid, scrip_id)
    )
    conn.commit()