import MySQLdb

connection = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="abolanle12@",
    db="attendance-system-python",
    port=3306  # Ensure the correct port here
)
cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print(f"Database version: {data}")
connection.close()