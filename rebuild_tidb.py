import pymysql, ssl, hashlib
ctx = ssl.create_default_context(cafile='tidb-ca.pem')
conn = pymysql.connect(host='gateway01.ap-northeast-1.prod.aws.tidbcloud.com', user='2bQTqZhCnsH42Ss.root', password='gNnYDF8UbAFqx0Br', port=4000, database='bhagalpur_stays', ssl=ctx)
c = conn.cursor()
# Drop all tables
c.execute("SET FOREIGN_KEY_CHECKS=0")
tables = ['audit_logs','bookings','coupon_usages','coupons','hotel_amenities','hotel_images','notifications','payments','reviews','room_images','room_inventory','room_types','wishlists','hotels','areas','amenities','owner_details','password_resets','refresh_tokens','users','cities']
for t in tables:
    try: c.execute(f"DROP TABLE IF EXISTS {t}")
    except: pass
c.execute("SET FOREIGN_KEY_CHECKS=1")
conn.commit()
print('All tables dropped. Recreating...')
# Create only essential tables with exact columns
c.execute("""
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(15),
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(10) DEFAULT 'guest',
  is_verified BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE cities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  state VARCHAR(100) DEFAULT 'Bihar',
  slug VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE hotels (
  id INT AUTO_INCREMENT PRIMARY KEY,
  owner_id INT NOT NULL,
  city_id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  slug VARCHAR(200) UNIQUE NOT NULL,
  description TEXT,
  full_address TEXT NOT NULL,
  star_rating INT DEFAULT 3,
  status VARCHAR(20) DEFAULT 'approved',
  is_featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE hotel_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  image_url VARCHAR(500) NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE room_types (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  bed_type VARCHAR(50),
  max_guests INT DEFAULT 2,
  base_price DECIMAL(10,2) NOT NULL,
  total_rooms INT DEFAULT 1,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_ref VARCHAR(20) UNIQUE NOT NULL,
  user_id INT NOT NULL,
  hotel_id INT NOT NULL,
  room_type_id INT NOT NULL,
  check_in DATE NOT NULL,
  check_out DATE NOT NULL,
  guests INT DEFAULT 2,
  guest_name VARCHAR(100),
  guest_email VARCHAR(150),
  guest_phone VARCHAR(15),
  base_amount DECIMAL(10,2) NOT NULL,
  tax_amount DECIMAL(10,2) DEFAULT 0,
  discount_amount DECIMAL(10,2) DEFAULT 0,
  total_amount DECIMAL(10,2) NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  payment_status VARCHAR(20) DEFAULT 'unpaid',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  hotel_id INT NOT NULL,
  rating INT NOT NULL,
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE wishlists (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  hotel_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE coupons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  discount_type VARCHAR(20) NOT NULL,
  discount_value DECIMAL(10,2) NOT NULL,
  min_booking_amount DECIMAL(10,2) DEFAULT 0,
  max_discount DECIMAL(10,2),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE payments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_method VARCHAR(20) DEFAULT 'pay_at_hotel',
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE refresh_tokens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  token VARCHAR(500) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE password_resets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  token VARCHAR(500) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE audit_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50),
  entity_id INT,
  ip_address VARCHAR(45),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  message TEXT,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
# Seed data
city_id = 1
c.execute("INSERT INTO cities (id, name, state, slug) VALUES (1, 'Bhagalpur', 'Bihar', 'bhagalpur')")
h = hashlib.sha256('Admin@123'.encode()).hexdigest()
c.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s,%s,%s,%s,%s,%s)", ('Admin', 'admin@bhagalpurstays.com', '8001234567', h, 'admin', True))
h2 = hashlib.sha256('Owner@123'.encode()).hexdigest()
c.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s,%s,%s,%s,%s,%s)", ('Owner', 'owner@bhagalpurstays.com', '9876543210', h2, 'owner', True))
hotels = [
    ('The Ganga Vilas Palace', 'ganga-vilas-palace', 'Adampur, Bhagalpur', 5, 1),
    ('Vikramshila Grand', 'vikramshila-grand', 'Tilkamanjhi, Bhagalpur', 4, 1),
    ('Silk City Inn', 'silk-city-inn', 'Nathnagar, Bhagalpur', 3, 0),
    ('Riverside Resort', 'riverside-resort-bhagalpur', 'Sultanganj Road, Bhagalpur', 5, 1),
    ('Hotel Kohinoor Residency', 'hotel-kohinoor-residency', 'Bhikhanpur, Bhagalpur', 3, 0),
    ('The Champa Boutique', 'champa-boutique', 'Barari, Bhagalpur', 4, 1),
    ('Business Suites', 'business-suites-bhagalpur', 'Court Road, Bhagalpur', 4, 0),
    ('Ganga View Homestay', 'ganga-view-homestay', 'Champanagar, Bhagalpur', 2, 0),
]
for name, slug, addr, stars, feat in hotels:
    c.execute("INSERT INTO hotels (owner_id, city_id, name, slug, full_address, star_rating, is_featured) VALUES (2, 1, %s, %s, %s, %s, %s)", (name, slug, addr, stars, feat))
coupons = [
    ('SILK500', 'fixed', 500, 2000, 500),
    ('WEEKEND10', 'percentage', 10, 3000, 1500),
    ('FIRST20', 'percentage', 20, 1500, 2000),
]
for code, dtype, dval, min_amt, max_disc in coupons:
    c.execute("INSERT INTO coupons (code, discount_type, discount_value, min_booking_amount, max_discount, is_active) VALUES (%s,%s,%s,%s,%s,1)", (code, dtype, dval, min_amt, max_disc))
conn.commit()
conn.close()
print('Database rebuilt and seeded successfully!')
