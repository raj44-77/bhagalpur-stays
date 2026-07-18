-- ============================================
-- Bhagalpur Stays — Database Schema
-- ============================================
CREATE DATABASE IF NOT EXISTS bhagalpur_stays
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE bhagalpur_stays;

-- ============================================
-- USERS & AUTH
-- ============================================
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(15) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('guest', 'owner', 'admin') DEFAULT 'guest',
  avatar_url VARCHAR(500),
  is_verified BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_users_email (email),
  INDEX idx_users_phone (phone),
  INDEX idx_users_role (role)
) ENGINE=InnoDB;

CREATE TABLE refresh_tokens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  token VARCHAR(500) NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_refresh_token (token)
) ENGINE=InnoDB;

CREATE TABLE password_resets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  token VARCHAR(500) NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  used BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_password_reset_token (token)
) ENGINE=InnoDB;

-- ============================================
-- OWNER DETAILS
-- ============================================
CREATE TABLE owner_details (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL UNIQUE,
  business_name VARCHAR(150),
  gst_number VARCHAR(20),
  pan_number VARCHAR(15),
  aadhaar_number VARCHAR(20),
  address TEXT,
  document_url VARCHAR(500),
  verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
  verified_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================
-- CITIES & LOCATIONS
-- ============================================
CREATE TABLE cities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  state VARCHAR(100) DEFAULT 'Bihar',
  slug VARCHAR(100) UNIQUE NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE areas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  city_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  slug VARCHAR(150) NOT NULL,
  pincode VARCHAR(10),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
  UNIQUE KEY unique_area (city_id, slug)
) ENGINE=InnoDB;

-- ============================================
-- HOTELS
-- ============================================
CREATE TABLE hotels (
  id INT AUTO_INCREMENT PRIMARY KEY,
  owner_id INT NOT NULL,
  city_id INT NOT NULL,
  area_id INT,
  name VARCHAR(200) NOT NULL,
  slug VARCHAR(200) UNIQUE NOT NULL,
  description TEXT,
  full_address TEXT NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  star_rating TINYINT DEFAULT 3 CHECK (star_rating BETWEEN 1 AND 5),
  contact_phone VARCHAR(15),
  contact_email VARCHAR(150),
  check_in_time TIME DEFAULT '14:00:00',
  check_out_time TIME DEFAULT '11:00:00',
  cancellation_hours INT DEFAULT 24,
  status ENUM('draft', 'pending', 'approved', 'rejected', 'suspended') DEFAULT 'draft',
  is_featured BOOLEAN DEFAULT FALSE,
  total_rooms INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (city_id) REFERENCES cities(id),
  FOREIGN KEY (area_id) REFERENCES areas(id) ON DELETE SET NULL,
  INDEX idx_hotels_owner (owner_id),
  INDEX idx_hotels_city (city_id),
  INDEX idx_hotels_status (status),
  INDEX idx_hotels_slug (slug)
) ENGINE=InnoDB;

CREATE TABLE hotel_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  image_url VARCHAR(500) NOT NULL,
  caption VARCHAR(200),
  sort_order INT DEFAULT 0,
  is_primary BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  INDEX idx_hotel_images (hotel_id)
) ENGINE=InnoDB;

CREATE TABLE hotel_policies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  policy_type VARCHAR(50) NOT NULL,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  INDEX idx_hotel_policies (hotel_id)
) ENGINE=InnoDB;

-- ============================================
-- AMENITIES
-- ============================================
CREATE TABLE amenities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  icon VARCHAR(50),
  category VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE hotel_amenities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  amenity_id INT NOT NULL,
  is_available BOOLEAN DEFAULT TRUE,
  extra_charge DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE,
  UNIQUE KEY unique_hotel_amenity (hotel_id, amenity_id)
) ENGINE=InnoDB;

-- ============================================
-- ROOMS
-- ============================================
CREATE TABLE room_types (
  id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  room_size_sqft INT,
  bed_type VARCHAR(50),
  max_guests INT DEFAULT 2,
  base_price DECIMAL(10,2) NOT NULL,
  extra_bed_price DECIMAL(10,2) DEFAULT 0,
  total_rooms INT DEFAULT 1,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  INDEX idx_room_types_hotel (hotel_id)
) ENGINE=InnoDB;

CREATE TABLE room_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_type_id INT NOT NULL,
  image_url VARCHAR(500) NOT NULL,
  caption VARCHAR(200),
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE room_inventory (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_type_id INT NOT NULL,
  date DATE NOT NULL,
  available_rooms INT NOT NULL DEFAULT 0,
  price_override DECIMAL(10,2),
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE,
  UNIQUE KEY unique_room_date (room_type_id, date),
  INDEX idx_inventory_date (date)
) ENGINE=InnoDB;

-- ============================================
-- BOOKINGS
-- ============================================
CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_ref VARCHAR(20) UNIQUE NOT NULL,
  user_id INT NOT NULL,
  hotel_id INT NOT NULL,
  room_type_id INT NOT NULL,
  check_in DATE NOT NULL,
  check_out DATE NOT NULL,
  number_of_rooms INT DEFAULT 1,
  guests INT DEFAULT 2,
  guest_name VARCHAR(100),
  guest_email VARCHAR(150),
  guest_phone VARCHAR(15),
  special_requests TEXT,
  nights INT GENERATED ALWAYS AS (DATEDIFF(check_out, check_in)) STORED,
  base_amount DECIMAL(10,2) NOT NULL,
  tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
  discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
  coupon_id INT,
  total_amount DECIMAL(10,2) NOT NULL,
  status ENUM('pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled', 'no_show') DEFAULT 'pending',
  payment_status ENUM('unpaid', 'partial', 'paid', 'refunded') DEFAULT 'unpaid',
  cancelled_at TIMESTAMP NULL,
  cancellation_reason TEXT,
  refund_amount DECIMAL(10,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (hotel_id) REFERENCES hotels(id),
  FOREIGN KEY (room_type_id) REFERENCES room_types(id),
  INDEX idx_bookings_user (user_id),
  INDEX idx_bookings_hotel (hotel_id),
  INDEX idx_bookings_status (status),
  INDEX idx_bookings_ref (booking_ref),
  INDEX idx_bookings_dates (check_in, check_out)
) ENGINE=InnoDB;

-- ============================================
-- PAYMENTS
-- ============================================
CREATE TABLE payments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT NOT NULL,
  user_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_method ENUM('upi', 'card', 'netbanking', 'wallet', 'cash', 'pay_at_hotel') DEFAULT 'pay_at_hotel',
  transaction_id VARCHAR(200),
  gateway_response JSON,
  status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending',
  paid_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_payments_booking (booking_id),
  INDEX idx_payments_status (status)
) ENGINE=InnoDB;

-- ============================================
-- REVIEWS
-- ============================================
CREATE TABLE reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  hotel_id INT NOT NULL,
  booking_id INT,
  rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  cleanliness_rating INT CHECK (cleanliness_rating BETWEEN 1 AND 5),
  service_rating INT CHECK (service_rating BETWEEN 1 AND 5),
  comfort_rating INT CHECK (comfort_rating BETWEEN 1 AND 5),
  value_rating INT CHECK (value_rating BETWEEN 1 AND 5),
  location_rating INT CHECK (location_rating BETWEEN 1 AND 5),
  title VARCHAR(200),
  comment TEXT,
  is_verified BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE SET NULL,
  UNIQUE KEY unique_user_booking_review (user_id, booking_id),
  INDEX idx_reviews_hotel (hotel_id),
  INDEX idx_reviews_rating (rating)
) ENGINE=InnoDB;

-- ============================================
-- WISHLISTS
-- ============================================
CREATE TABLE wishlists (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  hotel_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_hotel_wishlist (user_id, hotel_id)
) ENGINE=InnoDB;

-- ============================================
-- COUPONS
-- ============================================
CREATE TABLE coupons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  discount_type ENUM('percentage', 'fixed') NOT NULL,
  discount_value DECIMAL(10,2) NOT NULL,
  min_booking_amount DECIMAL(10,2) DEFAULT 0,
  max_discount DECIMAL(10,2),
  usage_limit INT DEFAULT 0,
  used_count INT DEFAULT 0,
  is_active BOOLEAN DEFAULT TRUE,
  valid_from DATE,
  valid_until DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_coupons_code (code)
) ENGINE=InnoDB;

CREATE TABLE coupon_usages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  coupon_id INT NOT NULL,
  user_id INT NOT NULL,
  booking_id INT NOT NULL,
  discount_amount DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (coupon_id) REFERENCES coupons(id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_booking_coupon (user_id, booking_id)
) ENGINE=InnoDB;

-- ============================================
-- NOTIFICATIONS
-- ============================================
CREATE TABLE notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  message TEXT,
  notification_type ENUM('booking', 'payment', 'review', 'promotion', 'system', 'owner') DEFAULT 'system',
  is_read BOOLEAN DEFAULT FALSE,
  link_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_notifications_user (user_id, is_read),
  INDEX idx_notifications_date (created_at)
) ENGINE=InnoDB;

-- ============================================
-- AUDIT LOGS
-- ============================================
CREATE TABLE audit_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50),
  entity_id INT,
  old_values JSON,
  new_values JSON,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  INDEX idx_audit_logs_user (user_id),
  INDEX idx_audit_logs_entity (entity_type, entity_id),
  INDEX idx_audit_logs_date (created_at)
) ENGINE=InnoDB;

-- ============================================
-- SEED DATA — Bhagalpur
-- ============================================
INSERT INTO cities (name, state, slug) VALUES ('Bhagalpur', 'Bihar', 'bhagalpur');

INSERT INTO areas (city_id, name, slug, pincode) VALUES
(1, 'Adampur', 'adampur', '812001'),
(1, 'Tilkamanjhi', 'tilkamanjhi', '812001'),
(1, 'Barari', 'barari', '812003'),
(1, 'Nathnagar', 'nathnagar', '812006'),
(1, 'Sultanganj', 'sultanganj', '813213'),
(1, 'Champanagar', 'champanagar', '812004'),
(1, 'Bhikhanpur', 'bhikhanpur', '812002'),
(1, 'Court Road', 'court-road', '812001');

INSERT INTO amenities (name, icon, category) VALUES
('Free WiFi', 'wifi', 'connectivity'),
('Parking', 'parking', 'facility'),
('Restaurant', 'restaurant', 'dining'),
('Breakfast', 'breakfast', 'dining'),
('Swimming Pool', 'pool', 'recreation'),
('Gym', 'gym', 'recreation'),
('Spa', 'spa', 'wellness'),
('AC', 'ac', 'comfort'),
('Room Service', 'service', 'service'),
('Pet Friendly', 'pet', 'policy'),
('Meeting Room', 'meeting', 'business'),
('Family Rooms', 'family', 'family');

-- Default coupons
INSERT INTO coupons (code, description, discount_type, discount_value, min_booking_amount, max_discount, usage_limit, valid_until) VALUES
('SILK500', 'Flat ₹500 off on first booking', 'fixed', 500, 2000, 500, 100, '2027-12-31'),
('WEEKEND10', '10% off on weekend stays', 'percentage', 10, 3000, 1500, 200, '2027-12-31'),
('FIRST20', '20% off for new users', 'percentage', 20, 1500, 2000, 50, '2027-12-31'),
('FAMILY50', '₹500 off on family rooms', 'fixed', 500, 4000, 500, 75, '2027-12-31');

-- Admin user (password: Admin@123)
INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES
('Admin Bhagalpur', 'admin@apnabhagalpur.com', '8001234567', '$2b$12$LJ3m4ys3Lk0TSwHCpNqrMOY7pEkM.mVZ4hGmZq9qHqCaPQqMsFUjm', 'admin', TRUE);