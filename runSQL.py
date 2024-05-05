import mysql.connector
# Create a connection to the database
db = mysql.connector.connect(
  host="localhost",  # replace with your host name
  user="root",  # replace with your username
  password="pass",  # replace with your password
  database="sakila"  # replace with your database name
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