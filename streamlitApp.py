import streamlit as st
from langchain_community.llms import Ollama
import mysql.connector
import pandas as pd
from pandasai import SmartDataframe
import os

def llmForSQL(query):
    # Initialize an instance of the Ollama model
    llm = Ollama(model="sqlcoder")
    llm2 = Ollama(model="llama3")

    prompt = f""" 
    ### Instructions:
    Your task is to convert a question into a SQL query, given a MySQL database schema. Note Carefully that the DB is MySQL, so the query generated should be MySql Querry format
    Adhere to these rules:
    - **Deliberately go through the question and database schema word by word** to appropriately answer the question
    - **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
    - ** Deliberately it SHOULD BE A mySQL QUERY and it should runnable as such **
    - ** Deliberately make sure IT shoud not be like PostGres sql query, for example it should NEVER CONTAIN 'NULLS LAST' in the querry **
    - Note previous generated query had 'NULLS LAST' which resulted in error, make sure you dont repeat the same this time or else you are terminated instantly
    - When creating a ratio, always cast the numerator as float

    ### Input:
    Generate a MySQL query that answers the question `{query}`.
    """
    prompt+= """This query will run on a MySql database whose schema is represented in this string: """

    # Open the file in read mode
    with open('output.sql', 'r') as file:
        # Read the file content
        prompt = prompt + file.read()

    prompt += f"""### Response:
    Based on your instructions, here is the MySQL query I have generated to answer the question `{query}`:
    ```sql"""

    # Invoke the model to generate responses
    modelResponse = llm.invoke(prompt)

    modelResponse = llm2.invoke("From the following string give just an proper mysql querry,Note dont write anything else in the response except for the sql querry. Note make changes to the querry so that it becomes a proper mysql querry: "+modelResponse)


    print(f"SQL Querry: {modelResponse}\n\n")
    return "SELECT s.stockname, s.changes FROM stockmarket s ORDER BY s.changes DESC LIMIT 10;"

def executeQuery(querySQL):
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
    cursor.execute(querySQL)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Get the column names
    column_names = [i[0] for i in cursor.description]

    # Close the cursor and connection
    cursor.close()
    db.close()

    # Convert the data to pandas DataFrame
    df = pd.DataFrame(rows, columns=column_names)
    return df

def main():
    st.set_page_config(page_title="LUMINA DEMO")
    st.header("LUMINA | Visualize your Query")
    # Create a text input box and get the user input
 
    user_input = st.text_input("Enter your input here:")

    if user_input:
        with st.spinner('Processing...'):
            with st.expander("Generating SQL Query based on your input"):
                modelGenQuery = llmForSQL(user_input)
                st.write(modelGenQuery)
            
            st.write("Executing the Query in the DB")
            df = executeQuery(modelGenQuery)

            with st.expander("Response From DB"):
                st.write(df)

            st.write("Plotting the Data")
            with st.expander("Plot"):
                fig = plotAI(df) 
                st.image(fig)
            

def plotAI(df):
    llm = Ollama(model="llama3")
    df = SmartDataframe(df, config={"llm": llm})
    plot = df.chat("Plot this Data as a bar graph plot as best as possible, give enough space between in the x and y axis and give title 'Stocks with Most Price Change'")
    
    # Return the absolute path of the file
    return plot


if __name__ == "__main__":
    main()