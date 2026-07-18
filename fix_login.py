import pymysql, ssl
ctx = ssl.create_default_context(cafile='tidb-ca.pem')
conn = pymysql.connect(host='gateway01.ap-northeast-1.prod.aws.tidbcloud.com', user='2bQTqZhCnsH42Ss.root', password='gNnYDF8UbAFqx0Br', port=4000, database='bhagalpur_stays', ssl=ctx)
c = conn.cursor()
hash = '.mVZ4hGmZq9qHqCaPQqMsFUjm'
c.execute("INSERT INTO users (full_name, email, phone, password_hash, role, is_verified) VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE password_hash=%s", ('Test', 'test@bhagalpur.com', '9999999999', hash, 'guest', True, hash))
conn.commit()
conn.close()
print('Done! Login: test@bhagalpur.com / Test@123')
