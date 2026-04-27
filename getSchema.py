import os
import mysql.connector

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'new_schema')

# Create a connection to the database
db = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DATABASE
)

# Create a cursor object
cursor = db.cursor()

# Get all table names
cursor.execute("SHOW TABLES")

# Fetch all the rows
tables = cursor.fetchall()

# Open the output file
with open('output.sql', 'w') as f:
  for table in tables:
    # Get the table name
    table_name = table[0]
    
    # Run SHOW CREATE TABLE for the table
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Write the CREATE TABLE statement to the file
    f.write(result[1] + ';\n\n')

# Close the connection
db.close()