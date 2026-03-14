import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db import get_db
from datetime import datetime, timedelta

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            company TEXT,
            role TEXT,
            balance REAL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS gov_registry (
            scripId TEXT PRIMARY KEY,
            type TEXT,
            faceValue REAL,
            expiryDate TEXT,
            currentOwnerUid TEXT,
            status TEXT DEFAULT 'with_exporter'
        );
        CREATE TABLE IF NOT EXISTS listings (
            listingId TEXT PRIMARY KEY,
            scripId TEXT,
            sellerId TEXT,
            type TEXT,
            faceValue REAL,
            askPrice REAL,
            discountRate REAL,
            expiryDate TEXT,
            status TEXT DEFAULT 'active',
            lockedByBuyerId TEXT DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS transactions (
            txnId TEXT PRIMARY KEY,
            listingId TEXT,
            scripId TEXT,
            buyerId TEXT,
            sellerId TEXT,
            faceValue REAL,
            agreedPrice REAL,
            commission REAL,
            escrowStatus TEXT,
            cancelledBy TEXT DEFAULT NULL,
            finedAmount REAL DEFAULT 0,
            fineReason TEXT DEFAULT NULL,
            createdAt TEXT
        );
        CREATE TABLE IF NOT EXISTS buyer_demands (
            demandId TEXT PRIMARY KEY,
            buyerId TEXT,
            scripType TEXT,
            minValue REAL,
            maxValue REAL,
            minExpiryDays INTEGER,
            status TEXT DEFAULT 'open',
            matchedListingId TEXT DEFAULT NULL,
            createdAt TEXT
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT,
            message TEXT,
            type TEXT,
            read INTEGER DEFAULT 0,
            createdAt TEXT
        );
    """)
    conn.commit()
    print("Tables created.")

def seed_users():
    conn = get_db()
    cursor = conn.cursor()
    sellers = [
        ("seller_01", "Alpha Exports Pvt Ltd",    "seller", 0),
        ("seller_02", "Beta Textiles Ltd",         "seller", 0),
        ("seller_03", "Gamma Garments Co",         "seller", 0),
        ("seller_04", "Delta Handicrafts Pvt Ltd", "seller", 0),
        ("seller_05", "Epsilon Engineering Ltd",   "seller", 0),
        ("seller_06", "Zeta Chemicals Ltd",        "seller", 0),
        ("seller_07", "Eta Pharma Exports",        "seller", 0),
        ("seller_08", "Theta Spices & Foods Ltd",  "seller", 0),
    ]
    buyers = [
        ("buyer_01", "Global Imports Ltd",        "buyer", 10000000),
        ("buyer_02", "Prime Traders Pvt Ltd",     "buyer", 7500000),
        ("buyer_03", "Apex Importers Co",         "buyer", 5000000),
        ("buyer_04", "Metro Commerce Ltd",        "buyer", 8000000),
        ("buyer_05", "National Traders Pvt Ltd",  "buyer", 6000000),
        ("buyer_06", "Sterling Imports Ltd",      "buyer", 9000000),
        ("buyer_07", "Horizon Trade Co",          "buyer", 4500000),
        ("buyer_08", "Pinnacle Importers Ltd",    "buyer", 7000000),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO users (uid, company, role, balance) VALUES (?, ?, ?, ?)",
        sellers + buyers
    )
    conn.commit()
    print(f"Seeded {len(sellers)} sellers and {len(buyers)} buyers.")

def seed_gov_registry():
    today = datetime.today()
    conn = get_db()
    cursor = conn.cursor()
    scrips = [
        ("RODTEP101", "RoDTEP", 500000,  (today + timedelta(days=400)).strftime("%Y-%m-%d"), "seller_01"),
        ("RODTEP102", "RoDTEP", 300000,  (today + timedelta(days=300)).strftime("%Y-%m-%d"), "seller_01"),
        ("ROSCTL101", "ROSCTL", 120000,  (today + timedelta(days=200)).strftime("%Y-%m-%d"), "seller_01"),
        ("RODTEP201", "RoDTEP", 750000,  (today + timedelta(days=350)).strftime("%Y-%m-%d"), "seller_02"),
        ("ROSCTL201", "ROSCTL", 200000,  (today + timedelta(days=180)).strftime("%Y-%m-%d"), "seller_02"),
        ("RODTEP301", "RoDTEP", 450000,  (today + timedelta(days=500)).strftime("%Y-%m-%d"), "seller_03"),
        ("ROSCTL301", "ROSCTL", 180000,  (today + timedelta(days=220)).strftime("%Y-%m-%d"), "seller_03"),
        ("RODTEP401", "RoDTEP", 600000,  (today + timedelta(days=450)).strftime("%Y-%m-%d"), "seller_04"),
        ("ROSCTL401", "ROSCTL", 250000,  (today + timedelta(days=160)).strftime("%Y-%m-%d"), "seller_04"),
        ("RODTEP501", "RoDTEP", 800000,  (today + timedelta(days=380)).strftime("%Y-%m-%d"), "seller_05"),
        ("ROSCTL501", "ROSCTL", 320000,  (today + timedelta(days=270)).strftime("%Y-%m-%d"), "seller_05"),
        ("RODTEP601", "RoDTEP", 350000,  (today + timedelta(days=420)).strftime("%Y-%m-%d"), "seller_06"),
        ("ROSCTL601", "ROSCTL", 150000,  (today + timedelta(days=190)).strftime("%Y-%m-%d"), "seller_06"),
        ("RODTEP701", "RoDTEP", 550000,  (today + timedelta(days=360)).strftime("%Y-%m-%d"), "seller_07"),
        ("ROSCTL701", "ROSCTL", 280000,  (today + timedelta(days=240)).strftime("%Y-%m-%d"), "seller_07"),
        ("RODTEP801", "RoDTEP", 420000,  (today + timedelta(days=480)).strftime("%Y-%m-%d"), "seller_08"),
        ("ROSCTL801", "ROSCTL", 220000,  (today + timedelta(days=210)).strftime("%Y-%m-%d"), "seller_08"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO gov_registry (scripId, type, faceValue, expiryDate, currentOwnerUid) VALUES (?, ?, ?, ?, ?)",
        scrips
    )
    conn.commit()
    print(f"Seeded {len(scrips)} scrips.")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("\nSeeding users...")
    seed_users()
    print("\nSeeding gov registry...")
    seed_gov_registry()
    print("\nDone! scriptradex.db is ready.")