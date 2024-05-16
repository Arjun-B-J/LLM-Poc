from langchain_community.llms import Ollama
import mysql.connector

# Initialize an instance of the Ollama model
llm = Ollama(model="sqlcoder")
llm2 = Ollama(model="llama3")


query = "I wanna see the top 10 stock name and their price change of those stocks who had most stock price changes"

prompt = f""" 
### Instructions:
Your task is to convert a question into a SQL query, given a MySQL database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- Should be able to run the query on mySQL DB, so dont include stuff like NULLS LAST or else THE PROGRAM DIES IMMEDIATELY
- When creating a ratio, always cast the numerator as float
- Note previous generated querry had NULLS LAST which resulted in error, make sure you dont repeat the same this time

### Input:
Generate a SQL query that answers the question `{query}`.
"""





prompt+= """This query will run on a database whose schema is represented in this string: """

# Open the file in read mode
with open('output.sql', 'r') as file:
    # Read the file content
    prompt = prompt + file.read()

prompt += f"""### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{query}`:
```sql"""

# Invoke the model to generate responses
modelResponse = llm.invoke(prompt)
print(f"Model Response: {modelResponse}")

modelResponse = llm2.invoke("From the following string give just an proper mysql querry,Note dont write anything else in the response except for the sql querry. Note make changes to the querry so that it becomes a proper mysql querry: "+modelResponse)


print(f"Model Generated SQL Querry: {modelResponse}\n\n")


# Create a connection to the database
db = mysql.connector.connect(
  host="localhost",  # replace with your host name
  user="root",  # replace with your username
  password="pass",  # replace with your password
  database="new_schema"  # replace with your database name
)

# Create a cursor object
cursor = db.cursor()

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
