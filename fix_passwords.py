import pymysql, ssl
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
admin_hash = pwd_context.hash('Admin@123')
owner_hash = pwd_context.hash('Owner@123')
ctx = ssl.create_default_context(cafile='tidb-ca.pem')
conn = pymysql.connect(host='gateway01.ap-northeast-1.prod.aws.tidbcloud.com', user='2bQTqZhCnsH42Ss.root', password='gNnYDF8UbAFqx0Br', port=4000, database='bhagalpur_stays', ssl=ctx)
c = conn.cursor()
c.execute("UPDATE users SET password_hash = %s WHERE email = %s", (admin_hash, 'admin@bhagalpurstays.com'))
c.execute("UPDATE users SET password_hash = %s WHERE email = %s", (owner_hash, 'owner@bhagalpurstays.com'))
conn.commit()
conn.close()
print('Passwords updated with bcrypt!')
