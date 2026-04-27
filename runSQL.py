import os
import mysql.connector

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'sakila')

# Create a connection to the database
db = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DATABASE
)

# Create a cursor object
cursor = db.cursor()

# Define your SQL query
query = """SELECT *
FROM actor
WHERE first_name LIKE 'A%';"""  # replace with your query

# Execute the query
cursor.execute(query)

# Fetch all the rows
rows = cursor.fetchall()

# Print all rows
for row in rows:
    print(row)

# Close the connection
db.close()