from mysql_db import get_connection
conn = get_connection()
print("Connection successful!")
conn.close()