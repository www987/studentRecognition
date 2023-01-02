import mariadb
import sys
try:
  conn = mariadb.connect(
    user="root",
    password="",
    host="localhost",
    database="studentsdatabase"
  )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor()
print(conn)