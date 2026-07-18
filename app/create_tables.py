"""Create all database tables directly via SQLAlchemy"""
from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:Raj%407744@localhost:3306/bhagalpur_stays"
engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as conn:
    # Drop existing tables (clean start)
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    
    # ============================================
    # USERS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(15) UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('guest','owner','admin') DEFAULT 'guest',
            avatar_url VARCHAR(500),
            is_verified BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB
    """))
    print("✅ Created: users")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS refresh_tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(500) NOT NULL UNIQUE,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: refresh_tokens")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(500) NOT NULL UNIQUE,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: password_resets")

    # ============================================
    # OWNER DETAILS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS owner_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL UNIQUE,
            business_name VARCHAR(150),
            gst_number VARCHAR(20),
            pan_number VARCHAR(15),
            aadhaar_number VARCHAR(20),
            address TEXT,
            document_url VARCHAR(500),
            verification_status ENUM('pending','verified','rejected') DEFAULT 'pending',
            verified_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: owner_details")

    # ============================================
    # CITIES & AREAS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            state VARCHAR(100) DEFAULT 'Bihar',
            slug VARCHAR(100) UNIQUE NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB
    """))
    print("✅ Created: cities")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS areas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_id INT NOT NULL,
            name VARCHAR(150) NOT NULL,
            slug VARCHAR(150) NOT NULL,
            pincode VARCHAR(10),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE,
            UNIQUE KEY unique_area (city_id, slug)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: areas")

    # ============================================
    # HOTELS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INT AUTO_INCREMENT PRIMARY KEY,
            owner_id INT NOT NULL,
            city_id INT NOT NULL,
            area_id INT,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200) UNIQUE NOT NULL,
            description TEXT,
            full_address TEXT NOT NULL,
            latitude DECIMAL(10,8),
            longitude DECIMAL(11,8),
            star_rating TINYINT DEFAULT 3,
            contact_phone VARCHAR(15),
            contact_email VARCHAR(150),
            check_in_time TIME DEFAULT '14:00:00',
            check_out_time TIME DEFAULT '11:00:00',
            cancellation_hours INT DEFAULT 24,
            status ENUM('draft','pending','approved','rejected','suspended') DEFAULT 'draft',
            is_featured BOOLEAN DEFAULT FALSE,
            total_rooms INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (city_id) REFERENCES cities(id),
            FOREIGN KEY (area_id) REFERENCES areas(id) ON DELETE SET NULL
        ) ENGINE=InnoDB
    """))
    print("✅ Created: hotels")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS hotel_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hotel_id INT NOT NULL,
            image_url VARCHAR(500) NOT NULL,
            caption VARCHAR(200),
            sort_order INT DEFAULT 0,
            is_primary BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: hotel_images")

    # ============================================
    # AMENITIES
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS amenities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            icon VARCHAR(50),
            category VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB
    """))
    print("✅ Created: amenities")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS hotel_amenities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hotel_id INT NOT NULL,
            amenity_id INT NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            extra_charge DECIMAL(10,2) DEFAULT 0,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
            FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE,
            UNIQUE KEY unique_hotel_amenity (hotel_id, amenity_id)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: hotel_amenities")

    # ============================================
    # ROOMS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS room_types (
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
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: room_types")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS room_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_type_id INT NOT NULL,
            image_url VARCHAR(500) NOT NULL,
            caption VARCHAR(200),
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: room_images")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS room_inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_type_id INT NOT NULL,
            date DATE NOT NULL,
            available_rooms INT NOT NULL DEFAULT 0,
            price_override DECIMAL(10,2),
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE,
            UNIQUE KEY unique_room_date (room_type_id, date)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: room_inventory")

    # ============================================
    # BOOKINGS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bookings (
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
            base_amount DECIMAL(10,2) NOT NULL,
            tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
            discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
            coupon_id INT,
            total_amount DECIMAL(10,2) NOT NULL,
            status ENUM('pending','confirmed','checked_in','checked_out','cancelled','no_show') DEFAULT 'pending',
            payment_status ENUM('unpaid','partial','paid','refunded') DEFAULT 'unpaid',
            cancelled_at TIMESTAMP NULL,
            cancellation_reason TEXT,
            refund_amount DECIMAL(10,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (hotel_id) REFERENCES hotels(id),
            FOREIGN KEY (room_type_id) REFERENCES room_types(id)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: bookings")

    # ============================================
    # PAYMENTS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT NOT NULL,
            user_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            payment_method ENUM('upi','card','netbanking','wallet','cash','pay_at_hotel') DEFAULT 'pay_at_hotel',
            transaction_id VARCHAR(200),
            gateway_response JSON,
            status ENUM('pending','success','failed','refunded') DEFAULT 'pending',
            paid_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: payments")

    # ============================================
    # REVIEWS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            hotel_id INT NOT NULL,
            booking_id INT,
            rating INT NOT NULL,
            cleanliness_rating INT,
            service_rating INT,
            comfort_rating INT,
            value_rating INT,
            location_rating INT,
            title VARCHAR(200),
            comment TEXT,
            is_verified BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
            FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE SET NULL,
            UNIQUE KEY unique_user_booking_review (user_id, booking_id)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: reviews")

    # ============================================
    # WISHLISTS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS wishlists (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            hotel_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_hotel_wishlist (user_id, hotel_id)
        ) ENGINE=InnoDB
    """))
    print("✅ Created: wishlists")

    # ============================================
    # COUPONS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS coupons (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            discount_type ENUM('percentage','fixed') NOT NULL,
            discount_value DECIMAL(10,2) NOT NULL,
            min_booking_amount DECIMAL(10,2) DEFAULT 0,
            max_discount DECIMAL(10,2),
            usage_limit INT DEFAULT 0,
            used_count INT DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            valid_from DATE,
            valid_until DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB
    """))
    print("✅ Created: coupons")

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS coupon_usages (
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
        ) ENGINE=InnoDB
    """))
    print("✅ Created: coupon_usages")

    # ============================================
    # NOTIFICATIONS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            message TEXT,
            notification_type ENUM('booking','payment','review','promotion','system','owner') DEFAULT 'system',
            is_read BOOLEAN DEFAULT FALSE,
            link_url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
    """))
    print("✅ Created: notifications")

    # ============================================
    # AUDIT LOGS
    # ============================================
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS audit_logs (
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
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        ) ENGINE=InnoDB
    """))
    print("✅ Created: audit_logs")

    # ============================================
    # SEED DATA
    # ============================================
    conn.execute(text("""
        INSERT INTO cities (name, state, slug) VALUES 
        ('Bhagalpur', 'Bihar', 'bhagalpur')
        ON DUPLICATE KEY UPDATE name=name
    """))
    print("✅ Seeded: cities")

    conn.execute(text("""
        INSERT INTO areas (city_id, name, slug, pincode) VALUES 
        (1, 'Adampur', 'adampur', '812001'),
        (1, 'Tilkamanjhi', 'tilkamanjhi', '812001'),
        (1, 'Barari', 'barari', '812003'),
        (1, 'Nathnagar', 'nathnagar', '812006'),
        (1, 'Sultanganj', 'sultanganj', '813213'),
        (1, 'Champanagar', 'champanagar', '812004'),
        (1, 'Bhikhanpur', 'bhikhanpur', '812002'),
        (1, 'Court Road', 'court-road', '812001')
        ON DUPLICATE KEY UPDATE name=name
    """))
    print("✅ Seeded: areas")

    conn.execute(text("""
        INSERT INTO amenities (name, icon, category) VALUES 
        ('Free WiFi', 'wifi', 'connectivity'),
        ('Parking', 'parking', 'facility'),
        ('Restaurant', 'restaurant', 'dining'),
        ('Breakfast', 'breakfast', 'dining'),
        ('Pool', 'pool', 'recreation'),
        ('Gym', 'gym', 'recreation'),
        ('Spa', 'spa', 'wellness'),
        ('AC', 'ac', 'comfort'),
        ('Room Service', 'service', 'service'),
        ('Pet Friendly', 'pet', 'policy'),
        ('Meeting Room', 'meeting', 'business'),
        ('Family Rooms', 'family', 'family')
        ON DUPLICATE KEY UPDATE name=name
    """))
    print("✅ Seeded: amenities")

    conn.execute(text("""
        INSERT INTO coupons (code, description, discount_type, discount_value, min_booking_amount, max_discount, usage_limit, valid_until) VALUES 
        ('SILK500', 'Flat Rs.500 off on first booking', 'fixed', 500, 2000, 500, 100, '2027-12-31'),
        ('WEEKEND10', '10% off on weekend stays', 'percentage', 10, 3000, 1500, 200, '2027-12-31'),
        ('FIRST20', '20% off for new users', 'percentage', 20, 1500, 2000, 50, '2027-12-31')
        ON DUPLICATE KEY UPDATE code=code
    """))
    print("✅ Seeded: coupons")

    conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    conn.commit()

print("\n🎉 All tables created and seeded successfully!")