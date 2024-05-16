import mysql.connector
# Create a connection to the database
db = mysql.connector.connect(
  host="localhost",  # replace with your host name
  user="root",  # replace with your username
  password="pass",  # replace with your password
  database="new_schema"  # replace with your database name
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