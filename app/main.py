"""Bhagalpur Stays - Main Application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import auth, hotels, rooms, bookings, payments, reviews, wishlist, dashboard, coupons, users
from app.middleware.rate_limit import rate_limit_middleware
from app.middleware.security_headers import security_headers_middleware

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bhagalpur Stays",
    description="Hotel booking platform for Bhagalpur, Bihar",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Middleware
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(security_headers_middleware)

# No-cache for HTML
@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response = await call_next(request)
    if not request.url.path.startswith('/api') and not request.url.path.startswith('/static'):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# API Routers
app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(reviews.router)
app.include_router(wishlist.router)
app.include_router(dashboard.router)

app.include_router(coupons.router)
app.include_router(users.router)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML Pages
@app.get("/")
def home(): return FileResponse("app/templates/index.html")
@app.get("/hotels")
def hotels_page(): return FileResponse("app/templates/hotels.html")
@app.get("/hotel-details")
def hotel_details(): return FileResponse("app/templates/hotel-details.html")
@app.get("/booking")
def booking_page(): return FileResponse("app/templates/booking.html")
@app.get("/login")
def login_page(): return FileResponse("app/templates/login.html")
@app.get("/signup")
def signup_page(): return FileResponse("app/templates/signup.html")
@app.get("/forgot-password")
def forgot_password_page(): return FileResponse("app/templates/forgot-password.html")
@app.get("/about")
def about_page(): return FileResponse("app/templates/about.html")
@app.get("/contact")
def contact_page(): return FileResponse("app/templates/contact.html")
@app.get("/faq")
def faq_page(): return FileResponse("app/templates/faq.html")
@app.get("/my-bookings")
def my_bookings_page(): return FileResponse("app/templates/my-bookings.html")
@app.get("/wishlist")
def wishlist_page(): return FileResponse("app/templates/wishlist.html")
@app.get("/offers")
def offers_page(): return FileResponse("app/templates/offers.html")
@app.get("/travel-guide")
def travel_guide_page(): return FileResponse("app/templates/travel-guide.html")
@app.get("/admin-dashboard")
def admin_dashboard_page(): return FileResponse("app/templates/admin-dashboard.html")
@app.get("/owner-dashboard")
def owner_dashboard_page(): return FileResponse("app/templates/owner-dashboard.html")
@app.get("/hotel-register")
def hotel_register_page(): return FileResponse("app/templates/hotel-register.html")
@app.get("/profile")
def profile_page(): return FileResponse("app/templates/profile.html")
@app.get("/privacy-policy")
def privacy_page(): return FileResponse("app/templates/privacy-policy.html")
@app.get("/terms")
def terms_page(): return FileResponse("app/templates/terms.html")
@app.get("/support")
def support_page(): return FileResponse("app/templates/support.html")
@app.get("/maintenance")
def maintenance_page(): return FileResponse("app/templates/maintenance.html")
@app.get("/404")
def not_found_page(): return FileResponse("app/templates/404.html")
@app.get("/health")
def health(): return {"status": "healthy"}