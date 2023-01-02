from login import login
from admin import admin
from user import user
from mysqlConnect import conn
from mysqlConnect import cur
ISADMIN = 100
USERID = 100
USERID, ISADMIN, = login()

if ISADMIN == 1:
    admin(USERID)
else:
    user(USERID)
conn.commit()
cur.close()
conn.close()
