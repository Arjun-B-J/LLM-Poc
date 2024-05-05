from langchain_community.llms import Ollama
import mysql.connector

# Initialize an instance of the Ollama model
llm = Ollama(model="llama3")

schema = ""
# Open the file in read mode
with open('output.sql', 'r') as file:
    # Read the file content
    schema = file.read()


query = "Get all details of all actors from the actor table whose name starts with letter A"

specialInstructions = ". Note just give output the query If you are unable to answer, output give unable to give for the current query"

#Formulating the querry
modelPrompt = "for the following sql schema <"+ schema + ">generate mySQL Querry for the following question <" + query + ">"
# Invoke the model to generate responses
modelResponse = llm.invoke(modelPrompt)
print(f"Model Response: {modelResponse}")

modelResponse = llm.invoke("from the following string give just an proper mysql querry,Note dont write anything else in the response except for the sql querry: "+modelResponse)


print(f"Model Generated SQL Querry: {modelResponse}\n\n")


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
query = """SELECT first_name, last_name
FROM actor
WHERE first_name LIKE 'A%' OR last_name LIKE 'A%';"""  # replace with your query

# Execute the query
cursor.execute(modelResponse)

# Fetch all the rows
rows = cursor.fetchall()

print("Running the SQL Querry\n\n")

# Print all rows
for row in rows:
    print(row)

# Close the connection
db.close()
