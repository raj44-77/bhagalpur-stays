import pymysql, hashlib
conn = pymysql.connect(host='reseau.proxy.rlwy.net', user='root', password='MpyQfBsJkMMhwWftRQjDnPzSPqNHNpod', port=20706, database='railway')
c = conn.cursor()
# Skip if already seeded
c.execute("SELECT COUNT(*) FROM users WHERE email='admin@bhagalpurstays.com'")
if c.fetchone()[0] > 0:
    print('Already seeded!')
    conn.close()
    exit()
h1 = hashlib.sha256('Admin@123'.encode()).hexdigest()
h2 = hashlib.sha256('Owner@123'.encode()).hexdigest()
c.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s,%s,%s,%s,%s,%s)", ('Admin', 'admin@bhagalpurstays.com', '8001234567', h1, 'admin', True))
c.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s,%s,%s,%s,%s,%s)", ('Owner', 'owner@bhagalpurstays.com', '9876543210', h2, 'owner', True))
# Check city exists
c.execute("SELECT id FROM cities WHERE slug='bhagalpur'")
city_id = c.fetchone()
if not city_id:
    c.execute("INSERT INTO cities (name, state, slug) VALUES ('Bhagalpur', 'Bihar', 'bhagalpur')")
    city_id = c.lastrowid
else:
    city_id = city_id[0]
hotels = [('The Ganga Vilas Palace','ganga-vilas-palace','Adampur, Bhagalpur',5,1),('Vikramshila Grand','vikramshila-grand','Tilkamanjhi, Bhagalpur',4,1),('Silk City Inn','silk-city-inn','Nathnagar, Bhagalpur',3,0),('Riverside Resort','riverside-resort-bhagalpur','Sultanganj Road, Bhagalpur',5,1),('Hotel Kohinoor Residency','hotel-kohinoor-residency','Bhikhanpur, Bhagalpur',3,0),('The Champa Boutique','champa-boutique','Barari, Bhagalpur',4,1),('Business Suites','business-suites-bhagalpur','Court Road, Bhagalpur',4,0),('Ganga View Homestay','ganga-view-homestay','Champanagar, Bhagalpur',2,0)]
for n,s,a,st,fe in hotels: 
    try: c.execute("INSERT INTO hotels (owner_id,city_id,name,slug,full_address,star_rating,is_featured,status) VALUES (2,%s,%s,%s,%s,%s,%s,%s)",(city_id,n,s,a,st,fe,'approved'))
    except: pass
for code,dtype,dval,min_amt,maxd in [('SILK500','fixed',500,2000,500),('WEEKEND10','percentage',10,3000,1500),('FIRST20','percentage',20,1500,2000)]:
    try: c.execute("INSERT INTO coupons (code,discount_type,discount_value,min_booking_amount,max_discount,is_active) VALUES (%s,%s,%s,%s,%s,1)",(code,dtype,dval,min_amt,maxd))
    except: pass
conn.commit()
conn.close()
print('Seeded successfully!')
