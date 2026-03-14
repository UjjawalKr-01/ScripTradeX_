# ⬡ ScripTradeX

> **India's first B2B marketplace for trading government-issued Duty Credit Scrips (RoDTEP & ROSCTL)**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)

---

## 📌 What is ScripTradeX?

Exporters in India receive **Duty Credit Scrips** (RoDTEP, ROSCTL) from the government as a rebate on taxes paid during export. These scrips can be used to offset import duties — but exporters often can't use them directly.

**ScripTradeX** bridges this gap:
- 🏭 **Sellers (Exporters)** list their scrips at a discount to get immediate liquidity
- 🏢 **Buyers (Importers)** purchase scrips below face value to reduce their customs duty burden
- 🔐 **Escrow protection** ensures neither party is exposed to fraud
- 💰 **1% platform commission** on every settled transaction

---

## ✨ Features

### 🏭 For Sellers
- Verify scrips against government registry (ICEGATE)
- List scrips with custom ask price and discount rate
- Receive buyer enquiries in **Deal Activity**
- Confirm or reject buyer requests
- Settle deals and receive payout instantly

### 🏢 For Buyers
- Place demands with scrip type, value range, and expiry preferences
- Automatic **matchmaking** against active listings
- Lock scrips and send enquiry to seller
- Pay via Card / UPI / Net Banking (mock gateway)
- Track deal status in **Deal Activity**

### 🛡️ Platform
- **Escrow engine** — funds held securely until both parties confirm
- **1% commission** deducted at settlement
- **Admin panel** — full commission ledger and transaction overview
- **AI Chatbot** — answers platform questions in real time
- **6-layer security** — rate limiting, IP blacklist, input sanitization, role enforcement, admin protection, request logging

---

## 🗂️ Project Structure

```
ScripTradeX/
│
├── 📄 run.py                     # App entry point
├── 📄 seed_data.py               # Database seeding (8 sellers, 8 buyers, 17 scrips)
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env                       # Environment variables (never commit)
├── 📄 .gitignore
├── 📄 README.md
│
└── 📁 app/
    ├── 📄 __init__.py            # App factory, blueprint registration
    ├── 📄 config.py              # Config from .env
    ├── 📄 db.py                  # SQLite connection
    ├── 📄 utils.py               # login_required decorator
    │
    ├── 📁 routes/
    │   ├── 📄 auth.py            # Login / Logout
    │   ├── 📄 seller.py          # Seller dashboard, list/delist scrip
    │   ├── 📄 buyer.py           # Buyer dashboard, place demand
    │   ├── 📄 marketplace.py     # Public marketplace with filters
    │   ├── 📄 escrow.py          # Full escrow state machine
    │   └── 📄 admin.py           # Admin panel (commission ledger)
    │
    ├── 📁 services/
    │   ├── 📄 gov_registry.py    # Scrip verification (ICEGATE mock)
    │   ├── 📄 matchmaking.py     # Demand → listing matching engine
    │   ├── 📄 escrow.py          # Escrow business logic
    │   └── 📄 commission.py      # 1% commission calculator
    │
    ├── 📁 templates/
    │   ├── 📄 base.html          # Base layout + navbar + chatbot
    │   ├── 📄 login.html         # Split seller/buyer login
    │   ├── 📄 seller_dashboard.html
    │   ├── 📄 buyer_dashboard.html
    │   ├── 📄 marketplace.html
    │   ├── 📄 payment.html       # Mock payment gateway
    │   ├── 📄 escrow_status.html
    │   └── 📄 admin_dashboard.html
    │
    └── 📁 static/
        └── 📄 main.css           # Stripe-inspired UI
```

---

## 🔄 Escrow Flow

```
Buyer clicks "Lock & Buy"
        ↓
  BUYER_INTERESTED  ──→  Seller sees enquiry in Deal Activity
        ↓                       ↓              ↓
        │                   Confirm          Reject
        │                     ↓                ↓
        │            SELLER_CONFIRMED     CANCELLED
        │                     ↓          (scrip relisted)
        │             Buyer pays via
        │            Card / UPI / NB
        │                     ↓
        │                FUNDS_HELD
        │                     ↓
        │            Seller clicks Settle
        │                     ↓
        └──────────────→  SETTLED ✅
                     (scrip transferred,
                      seller paid minus 1%)
```

---

## 🗃️ Database Schema

| Table | Description |
|---|---|
| `users` | Sellers and buyers with wallet balance |
| `gov_registry` | Government scrip registry (ICEGATE mock) |
| `listings` | Active scrip listings from sellers |
| `transactions` | Escrow transactions with full state |
| `buyer_demands` | Buyer demand parameters for matchmaking |
| `notifications` | Platform notifications (stored) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ScripTradeX.git
cd ScripTradeX

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install flask python-dotenv

# 5. Create .env file
echo FLASK_SECRET_KEY=scriptradex-secret-key > .env
echo FLASK_ENV=development >> .env
echo DATABASE_PATH=scriptradex.db >> .env

# 6. Seed the database
python seed_data.py

# 7. Run the app
python run.py
```

Open your browser at → **http://127.0.0.1:5000**

---

## 🔑 Demo Credentials

No passwords required. Select from dropdown on login page.

| Role | Example Accounts |
|---|---|
| 🏭 Seller | Alpha Exports Pvt Ltd → Theta Spices & Foods Ltd (8 sellers) |
| 🏢 Buyer | Global Imports Ltd → Pinnacle Importers Ltd (8 buyers, ₹50L–₹1Cr wallet) |
| 🔐 Admin | Visit `/admin/login` directly |

---

## 🧪 Testing the Full Flow

1. **Login as Seller** → List a scrip (set ask price below face value)
2. **Login as Buyer** → Place a demand → matching scrips appear → Lock & Buy
3. **Login as Seller** → Deal Activity → Confirm or Reject
4. **Login as Buyer** → Deal Activity → Pay Now → fill mock payment
5. **Login as Seller** → Deal Activity → Settle
6. **Visit `/admin/login`** → see commission ledger

---

## 🛡️ Security Layers

| Layer | Protection |
|---|---|
| 1️⃣ Rate Limiting | Max 10 login attempts per minute per IP |
| 2️⃣ IP Blacklist | Auto-block after 5 failed login attempts |
| 3️⃣ Input Sanitization | All POST inputs scanned for SQL injection & XSS |
| 4️⃣ Admin Protection | Secret key required for admin panel |
| 5️⃣ Role Enforcement | Buyers cannot access seller routes and vice versa |
| 6️⃣ Request Logger | Every request logged with IP, user, and timestamp |

---

## 💡 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python Flask |
| Database | SQLite |
| Frontend | Bootstrap 5 + Jinja2 |
| Fonts | Syne + DM Sans (Google Fonts) |
| UI Style | Stripe-inspired design system |
| Auth | Session-based (Flask sessions) |
| Security | Flask-Limiter + custom middleware |

---

## 🗺️ Roadmap

- [ ] Real ICEGATE API integration
- [ ] Blockchain scrip ownership ledger
- [ ] Smart contract escrow
- [ ] Real payment gateway (Razorpay/Stripe)
- [ ] Push notifications
- [ ] Admin analytics dashboard
- [ ] Mobile app

---

## 🏗️ Architecture Note — Why Not Blockchain?

ScripTradeX is built on a traditional stack for **MVP speed and demo reliability**. The natural production evolution is:

- 📒 **Scrip transfers** → immutable blockchain ledger
- 🔐 **Escrow** → smart contracts (auto-execute on condition)
- 🏛️ **ICEGATE** → trusted oracle feeding verified scrip data on-chain
- 🚫 **Double-selling fraud** → mathematically impossible on-chain

---

## 👨‍💻 Built With ❤️ for Indian FinTech

> *ScripTradeX addresses a real gap in India's EXIM ecosystem — bringing transparency, speed, and trust to a market that currently runs on phone calls and Excel sheets.*

---

## 📄 License

MIT License — free to use, modify, and distribute.
