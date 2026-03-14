# ⬡ ScripTradeX

> **India's First Centralised B2B Duty Credit Scrip Exchange Platform**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 📌 Problem Statement

India's exporters receive **Duty Credit Scrips** (RoDTEP, ROSCTL) from the government as a rebate on taxes paid during the export process. These scrips can be used to offset import customs duties — but most exporters cannot use them directly and are forced to sell them through unorganised brokers, phone calls, and Excel sheets.

Importers, on the other hand, are constantly looking for scrips to reduce their customs duty burden but have no verified, transparent platform to find them.

**The result:** A fragmented, opaque, and fraud-prone secondary market worth thousands of crores annually.

**ScripTradeX solves this** — a centralised, verified, escrow-protected B2B marketplace for trading duty credit scrips.

---

## 🔗 Blockchain Relevance

> **This problem statement directly maps to blockchain architecture.**

While ScripTradeX is currently built on a traditional Flask + SQLite stack for MVP speed and demo reliability, every core component of this platform is a natural fit for blockchain:

| ScripTradeX Component | Blockchain Equivalent |
|---|---|
| Gov Registry Verification | ICEGATE as a trusted on-chain oracle |
| Scrip Ownership Transfer | Immutable NFT-based ledger entry |
| Escrow Engine | Smart contract auto-executing on conditions |
| Commission Deduction | Programmatic on-chain fee at settlement |
| Penalty System | Smart contract enforced fine on delay |
| Transaction History | Append-only distributed ledger |
| Double-Selling Prevention | Cryptographically impossible on-chain |

**Why traditional stack for now?**
Building on blockchain at hackathon speed introduces wallet integration complexity, gas fee unpredictability, and testnet reliability issues that would compromise the demo. The architecture was designed with blockchain migration in mind — every service maps 1:1 to a smart contract.

**Production roadmap on blockchain:**
- Scrip issuance → ERC-1155 tokens on a permissioned chain
- Escrow → Solidity smart contract with automatic release conditions
- ICEGATE → Chainlink oracle feeding verified scrip data on-chain
- Penalty enforcement → on-chain timer with automatic fine deduction
- Double-selling fraud → mathematically impossible on-chain

---

## ✨ Complete Feature List

### 🏠 Landing Page
- Animated dark hero section with floating orbs and dot grid overlay
- Platform tagline, feature pills, and dual CTA buttons
- Stats bar — scrips available, active companies, fee, escrow protection
- 6 USP cards with hover animations and colour-coded accent bars
- 4-step "How It Works" flow with gradient progress line
- Footer CTA with redirect to login

### 🔐 Authentication
- Split login portal — separate Seller and Buyer panels with toggle tabs
- Dark navy background matching landing page theme
- Password protection (demo password: `demo123`)
- Eye icon toggle for password visibility
- Wrong password shows inline error with hint
- Role-based session management
- Logout redirects to landing page

### 🏭 Seller Dashboard
- Gradient stat cards — Active Listings, Pending Enquiries, Total Deals
- **Tabbed interface** — Listed Scrips tab and Deal Activity tab
- List New Scrip via modal — select from gov registry, set ask price
- ICEGATE scrip verification before listing
- Auto discount rate calculation
- Delist active scrips
- Deal Activity shows full pipeline — enquiry → confirm/reject → awaiting payment → settle
- Confirm or Reject buyer enquiries directly from dashboard
- Settle button appears when funds are held in escrow

### 🏢 Buyer Dashboard
- Gradient stat cards — Wallet Balance, Open Demands, Total Deals
- **Tabbed interface** — Find Scrips tab and Deal Activity tab
- Place Demand form — scrip type, min/max value, min days to expiry
- Instant matchmaking engine — returns best matches ranked by discount
- Matched scrip cards with face value, ask price, savings highlight, expiry
- Lock & Buy sends enquiry to seller instantly
- Deal Activity tracks full pipeline — awaiting seller, approved, payment done, settled, rejected
- **Penalty Notices section** — shows fines applied for settlement delays

### 🛍️ Marketplace
- Public listing of all active verified scrips
- Filters — scrip type, min/max value, min days to expiry
- Colour-coded scrip type badges (RoDTEP = blue, ROSCTL = pink)
- Direct Lock & Buy for logged-in buyers
- Empty state with clear filters option

### 🔐 Escrow Engine
- Full state machine: `BUYER_INTERESTED → SELLER_CONFIRMED → FUNDS_HELD → SETTLED`
- Cancellation at any stage with automatic scrip relisting
- Buyer refund on cancellation if funds were held
- `cancelledBy` tracking — distinguishes seller rejection from buyer cancellation
- Escrow status page with visual progress tracker

### 💳 Payment Gateway (Mock)
- Order summary with face value, commission breakdown, total due
- Three payment modes — Credit/Debit Card, UPI, Net Banking
- Card number auto-formatting (groups of 4)
- Processing state on submit button
- SSL Secured badge
- Cancel transaction option

### 💰 Commission System
- **1% platform commission** on every settled transaction
- Deducted from seller payout at settlement
- Visible only to admin — not shown to buyers or sellers

### ⚠️ Penalty & Fine System
- **5% fine** on scrip face value if scrip expires within 30 days at time of settlement
- **10% fine** on scrip face value if scrip has already expired at time of settlement
- Fine automatically deducted from buyer's wallet balance
- Seller notified of settlement, buyer notified of fine with reason
- Fine details visible on buyer dashboard under Penalty Notices
- Complete fine ledger visible on admin panel

### 🤖 AI Chatbot Assistant
- Floating chat bubble on every page
- 20+ question types covered — RoDTEP, ROSCTL, escrow, matchmaking, commission, login, payment, deal activity, rejection, settlement, expiry, face value, ICEGATE, marketplace
- Instant FAQ-style responses — no API calls, zero latency
- Styled message bubbles with user/bot distinction

### 🔒 Admin Panel (`/admin/login`)
- **6-Layer Security Infrastructure** display with pulsing active indicators
- Revenue Stats — Total Commission Earned, Total Transaction Volume, Settled Transactions
- Transaction Status Breakdown table
- Commission Ledger — full per-transaction breakdown with buyer, seller, face value, agreed price, 1% commission, seller payout
- **Penalty Ledger** — all fines collected with reason and amount
- Exit Admin button

### 🛡️ Security System (6 Layers)

| Layer | Protection |
|---|---|
| 1️⃣ Rate Limiting | Max 10 login attempts per minute per IP |
| 2️⃣ IP Blacklist | Auto-block after 5 failed login attempts |
| 3️⃣ Input Sanitization | All POST inputs scanned for SQL injection & XSS |
| 4️⃣ Admin Protection | Secret key session required for admin panel |
| 5️⃣ Role Enforcement | Buyers cannot access seller routes and vice versa |
| 6️⃣ Request Logger | Every request logged with IP, user, and timestamp |

---

## 🗂️ Project Structure

```
ScripTradeX/
│
├── 📄 run.py                        # App entry point
├── 📄 seed_data.py                  # Database seeding (8 sellers, 8 buyers, 17 scrips)
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env                          # Environment variables (never commit)
├── 📄 .gitignore
├── 📄 README.md
│
└── 📁 app/
    ├── 📄 __init__.py               # App factory, blueprint registration
    ├── 📄 config.py                 # Config from .env
    ├── 📄 db.py                     # SQLite connection
    ├── 📄 utils.py                  # login_required decorator
    │
    ├── 📁 routes/
    │   ├── 📄 auth.py               # Landing, Login, Logout
    │   ├── 📄 seller.py             # Seller dashboard, list/delist scrip
    │   ├── 📄 buyer.py              # Buyer dashboard, place demand
    │   ├── 📄 marketplace.py        # Public marketplace with filters
    │   ├── 📄 escrow.py             # Full escrow state machine
    │   └── 📄 admin.py              # Admin panel — commission + penalty ledger
    │
    ├── 📁 services/
    │   ├── 📄 gov_registry.py       # Scrip verification (ICEGATE mock)
    │   ├── 📄 matchmaking.py        # Demand → listing matching engine
    │   ├── 📄 escrow.py             # Escrow business logic
    │   ├── 📄 commission.py         # 1% commission calculator
    │   └── 📄 fine.py               # 5-10% penalty engine for delayed settlement
    │
    ├── 📁 templates/
    │   ├── 📄 landing.html          # Landing page with animations
    │   ├── 📄 base.html             # Base layout + navbar + chatbot + security badge
    │   ├── 📄 login.html            # Split seller/buyer login
    │   ├── 📄 seller_dashboard.html # Tabbed seller interface
    │   ├── 📄 buyer_dashboard.html  # Tabbed buyer interface with penalty notices
    │   ├── 📄 marketplace.html      # Filtered scrip listings
    │   ├── 📄 payment.html          # Mock payment gateway
    │   ├── 📄 escrow_status.html    # Escrow progress tracker
    │   └── 📄 admin_dashboard.html  # Admin panel with security + ledger
    │
    └── 📁 static/
        └── 📄 main.css              # Stripe-inspired design system
```

---

## 🔄 Escrow State Machine

```
Buyer clicks "Lock & Buy"
        ↓
  BUYER_INTERESTED ──────────────→ Seller sees enquiry in Deal Activity
        │                                    ↓               ↓
        │                               Confirm           Reject
        │                                 ↓                 ↓
        │                        SELLER_CONFIRMED       CANCELLED
        │                                 ↓           (scrip relisted,
        │                        Buyer pays via         cancelledBy
        │                       Card/UPI/Net Bkg        = sellerId)
        │                                 ↓
        │                           FUNDS_HELD
        │                                 ↓
        │                   Fine check (5% or 10% if
        │                   scrip near/past expiry)
        │                                 ↓
        │                        Seller clicks Settle
        │                                 ↓
        └──────────────────────→      SETTLED ✅
                              (scrip transferred,
                               seller paid minus 1%,
                               fine deducted from buyer
                               if applicable)
```

---

## 🗃️ Database Schema

| Table | Key Columns | Description |
|---|---|---|
| `users` | uid, company, role, balance | Sellers and buyers with wallet |
| `gov_registry` | scripId, type, faceValue, expiryDate, currentOwnerUid, status | ICEGATE mock registry |
| `listings` | listingId, scripId, sellerId, askPrice, discountRate, status | Active scrip listings |
| `transactions` | txnId, escrowStatus, cancelledBy, finedAmount, fineReason | Full escrow + fine tracking |
| `buyer_demands` | demandId, scripType, minValue, maxValue, minExpiryDays | Matchmaking parameters |
| `notifications` | uid, message, type, read | Platform notifications |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/UjjawalKr-01/ScripTradeX.git
cd ScripTradeX

# 2. Create virtual environment
python -m venv venv

# 3. Activate
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

# 7. Run
python run.py
```

Open → **http://127.0.0.1:5000**

---

## 🔑 Demo Credentials

| Role | Companies | Password |
|---|---|---|
| 🏭 Seller | Alpha Exports → Theta Spices (8 sellers) | `demo123` |
| 🏢 Buyer | Global Imports → Pinnacle Importers (8 buyers, ₹50L–₹1Cr wallet) | `demo123` |
| 🔐 Admin | Visit `/admin/login` directly | No password needed |

---

## 🧪 Full Demo Flow

```
1. Visit http://127.0.0.1:5000       → Landing page
2. Click "Enter Platform"            → Login page
3. Login as Seller (demo123)         → List a scrip, set ask price below face value
4. Login as Buyer (demo123)          → Place demand → matches appear → Lock & Buy
5. Login as Seller                   → Deal Activity tab → Confirm
6. Login as Buyer                    → Deal Activity tab → Pay Now → fill payment
7. Login as Seller                   → Deal Activity tab → Settle
8. Visit /admin/login                → Commission ledger + Security + Penalty ledger
```

---

## 💡 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python Flask |
| Database | SQLite (production → PostgreSQL) |
| Frontend | Bootstrap 5 + Jinja2 |
| Fonts | Syne (headings) + DM Sans (body) |
| UI Style | Stripe-inspired design system |
| Auth | Flask session-based |
| Security | Custom middleware (6-layer) |

---

## 🗺️ Production Roadmap

- [ ] Real ICEGATE API integration
- [ ] PostgreSQL migration
- [ ] Blockchain — ERC-1155 scrip tokens on permissioned chain
- [ ] Smart contract escrow (Solidity)
- [ ] Chainlink oracle for ICEGATE verification
- [ ] Real payment gateway (Razorpay / Stripe)
- [ ] Push notifications
- [ ] Mobile app (React Native)
- [ ] KYC / AML compliance layer
- [ ] Multi-language support (Hindi, Gujarati, Tamil)

---

## 👨‍💻 Built With ❤️ for India's EXIM Ecosystem

> *ScripTradeX addresses a real, high-value gap in India's trade finance infrastructure — replacing phone calls, brokers, and Excel sheets with a transparent, verified, and secure digital exchange.*

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*© 2025 ScripTradeX · Built for India's EXIM Ecosystem · All transactions escrow-protected*
