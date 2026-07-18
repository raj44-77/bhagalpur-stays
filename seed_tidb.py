import pymysql
import ssl
import hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
ssl_context = ssl.create_default_context(cafile='tidb-ca.pem')
conn = pymysql.connect(
    host='gateway01.ap-northeast-1.prod.aws.tidbcloud.com',
    user='2bQTqZhCnsH42Ss.root',
    password='gNnYDF8UbAFqx0Br',
    port=4000,
    database='bhagalpur_stays',
    ssl=ssl_context
)
cursor = conn.cursor()
# City
cursor.execute("INSERT INTO cities (name, state, slug) VALUES ('Bhagalpur', 'Bihar', 'bhagalpur')")
city_id = cursor.lastrowid
# Users
cursor.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s, %s, %s, %s, %s, %s)",
    ('Admin Bhagalpur', 'admin@bhagalpurstays.com', '8001234567', hash_password('Admin@123'), 'admin', True))
cursor.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s, %s, %s, %s, %s, %s)",
    ('Raj Hotel Owner', 'owner@bhagalpurstays.com', '9876543210', hash_password('Owner@123'), 'owner', True))
owner_id = cursor.lastrowid
# Hotels
hotels = [
    ('The Ganga Vilas Palace', 'ganga-vilas-palace', 'Adampur, Bhagalpur', 5, 1),
    ('Vikramshila Grand', 'vikramshila-grand', 'Tilkamanjhi, Bhagalpur', 4, 1),
    ('Silk City Inn', 'silk-city-inn', 'Nathnagar, Bhagalpur', 3, 0),
    ('Riverside Resort Bhagalpur', 'riverside-resort-bhagalpur', 'Sultanganj Road, Bhagalpur', 5, 1),
    ('Hotel Kohinoor Residency', 'hotel-kohinoor-residency', 'Bhikhanpur, Bhagalpur', 3, 0),
    ('The Champa Boutique', 'champa-boutique', 'Barari, Bhagalpur', 4, 1),
    ('Business Suites Bhagalpur', 'business-suites-bhagalpur', 'Court Road, Bhagalpur', 4, 0),
    ('Ganga View Homestay', 'ganga-view-homestay', 'Champanagar, Bhagalpur', 2, 0),
]
for h in hotels:
    cursor.execute(
        "INSERT INTO hotels (owner_id, city_id, name, slug, full_address, star_rating, status, is_featured) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (owner_id, city_id, h[0], h[1], h[2], h[3], 'approved', h[4])
    )
# Coupons
coupons = [
    ('SILK500', 'Flat Rs.500 off', 'fixed', 500, 2000, 500),
    ('WEEKEND10', '10% off weekends', 'percentage', 10, 3000, 1500),
    ('FIRST20', '20% off for new users', 'percentage', 20, 1500, 2000),
]
for c in coupons:
    cursor.execute(
        "INSERT INTO coupons (code, description, discount_type, discount_value, min_booking_amount, max_discount, is_active, valid_until) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (c[0], c[1], c[2], c[3], c[4], c[5], 1, '2027-12-31')
    )
conn.commit()
conn.close()
print('TiDB seeded successfully!')
