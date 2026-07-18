# 🏨 Bhagalpur Stays

**The #1 Hotel Booking Platform for Bhagalpur, Bihar**

Bhagalpur Stays is a full-stack hotel booking SaaS platform built for the Silk City. Discover, compare and book verified hotels across Bhagalpur — from luxury riverfront resorts to cozy homestays.

---

## 🚀 Features

### For Travelers
- 🔍 **Search & Filter** — Find hotels by price, star rating, area, and amenities
- 🏨 **Hotel Listings** — Browse 8 verified hotels with real images
- 📋 **Hotel Details** — View rooms, amenities, photos, reviews & policies
- 📅 **Smart Booking** — Select dates, rooms, guests — dynamic pricing
- 🎟️ **Coupons** — Apply discount codes (SILK500, WEEKEND10, FIRST20)
- ❤️ **Wishlist** — Save favorite hotels
- ⭐ **Reviews** — Rate and review completed stays
- 👤 **Profile** — Manage account, change password

### For Hotel Owners
- 📊 **Partner Dashboard** — Real-time revenue, bookings & occupancy
- 💰 **Revenue Tracking** — Mark bookings as paid, track earnings
- 🏨 **Hotel Management** — View all your hotels and their performance

### For Admins
- 🛡️ **Admin Dashboard** — Platform-wide KPIs, weekly charts
- ✅ **Approval System** — Review and approve new hotel registrations
- 👥 **User Management** — View all users and bookings

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.13 + FastAPI |
| **Database** | MySQL + SQLAlchemy ORM |
| **Authentication** | JWT (Access + Refresh Tokens) |
| **Password Hashing** | bcrypt via passlib |
| **Frontend** | Vanilla HTML5 + CSS3 + JavaScript |
| **CSS Framework** | Custom design system with CSS variables |
| **Icons** | Inline SVGs |
| **Images** | Real Bhagalpur landmark photos |
| **Server** | Uvicorn (ASGI) |

---

## 📁 Project Structure
Bhagalpur Stays/
├── app/
│ ├── main.py # FastAPI application
│ ├── database.py # SQLAlchemy connection
│ ├── security.py # JWT + password hashing
│ ├── config.py # App configuration
│ ├── constants.py # Constants
│ ├── dependencies.py # Dependencies
│ ├── routers/ # API routes
│ │ ├── auth.py # Signup, login, reset password
│ │ ├── hotels.py # Hotel listing & details
│ │ ├── rooms.py # Room types & availability
│ │ ├── bookings.py # Create, view, cancel bookings
│ │ ├── payments.py # Payment processing
│ │ ├── reviews.py # Submit & view reviews
│ │ ├── wishlist.py # Add & remove wishlist
│ │ ├── coupons.py # Validate & apply coupons
│ │ ├── dashboard.py # Admin & owner dashboards
│ │ ├── notifications.py # User notifications
│ │ └── users.py # User profile management
│ ├── models/ # SQLAlchemy models (18 models)
│ ├── schemas/ # Pydantic validation schemas
│ ├── services/ # Business logic layer
│ ├── middleware/ # Auth middleware
│ ├── utils/ # Helper utilities
│ ├── templates/ # HTML pages (27 pages)
│ └── static/ # CSS, JS, images
│ ├── css/ # 10 stylesheets
│ ├── js/ # JavaScript modules
│ └── images/ # Images & attractions
├── database/
│ ├── schema.sql # MySQL schema
│ └── seed.sql # Seed data
├── tests/ # Test files
├── .env # Environment variables
├── requirements.txt # Python dependencies
├── run.py # Server entry point
└── README.md # This file

text

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- pip

### Step 1: Clone & Setup

```bash
git clone https://github.com/yourusername/bhagalpur-stays.git
cd bhagalpur-stays
Step 2: Install Dependencies
bash
pip install -r requirements.txt
Step 3: Configure Environment
Create .env file:

env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/bhagalpur_stays
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=True
Step 4: Create Database
bash
mysql -u root -p -e "CREATE DATABASE bhagalpur_stays CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
Step 5: Seed Data
bash
python app/create_tables.py
Step 6: Run Server
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Open http://localhost:8000 in your browser.

🔑 Demo Credentials
Role	Email	Password	Dashboard
Admin	admin@apnabhagalpur.com	Admin@123	/admin-dashboard
Owner	owner@bhagalpurstays.com	Owner@123	/owner-dashboard
Guest	Create your own	/signup	/my-bookings
📡 API Endpoints
Auth
Method	Endpoint	Description
POST	/api/auth/signup	Register new user
POST	/api/auth/login	Login & get tokens
POST	/api/auth/refresh	Refresh access token
POST	/api/auth/forgot-password	Request password reset
POST	/api/auth/reset-password	Reset password
POST	/api/auth/logout	Logout
Hotels
Method	Endpoint	Description
GET	/api/hotels/	List hotels (with filters)
GET	/api/hotels/{slug}	Hotel details
Rooms
Method	Endpoint	Description
GET	/api/rooms/hotel/{hotel_id}	Hotel room types
GET	/api/rooms/{room_type_id}/availability	Check availability
Bookings
Method	Endpoint	Description
POST	/api/bookings/	Create booking
GET	/api/bookings/	My bookings
POST	/api/bookings/{id}/cancel	Cancel booking
Reviews
Method	Endpoint	Description
POST	/api/reviews/	Submit review
GET	/api/reviews/hotel/{hotel_id}	Hotel reviews
Wishlist
Method	Endpoint	Description
GET	/api/wishlist/	My wishlist
POST	/api/wishlist/{hotel_id}	Add to wishlist
DELETE	/api/wishlist/{hotel_id}	Remove from wishlist
Dashboard
Method	Endpoint	Description
GET	/api/dashboard/admin	Admin KPIs
GET	/api/dashboard/owner	Owner KPIs
Coupons
Method	Endpoint	Description
GET	/api/coupons/validate	Validate coupon
GET	/api/coupons/	Active coupons
Users
Method	Endpoint	Description
GET	/api/users/me	My profile
PUT	/api/users/me	Update profile
POST	/api/users/change-password	Change password
Payments
Method	Endpoint	Description
POST	/api/payments/mark-paid/{booking_id}	Mark booking as paid
🎨 Design System
Primary: Deep Navy (#1e3a8a)

Accent: Gold (#d4a437) — Silk City theme

Fonts: Playfair Display (headings) + Inter (body)

Dark Mode: Full support with CSS variables

Icons: Inline SVGs (no external icon fonts)

Responsive: Mobile-first with breakpoints at 500px, 700px, 900px, 1080px

🐛 Known Issues
Coupon code causes 500 error when booking (to be fixed)

Static file caching requires hard refresh on changes

Email service not configured (reset tokens shown in console)

📝 License
© 2026 Bhagalpur Stays. All rights reserved.

👨‍💻 Developer
Built with ❤️ for Bhagalpur, Bihar — The Silk City of India.

text
