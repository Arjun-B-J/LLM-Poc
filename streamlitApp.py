import streamlit as st
from langchain_community.llms import Ollama
import mysql.connector
import pandas as pd
from pandasai import SmartDataframe
import os

def llmForSQL(query):
    return """SELECT t1.CUSIP, (t2.price - t1.price) AS margin
FROM Trades t1
INNER JOIN Trace t2 ON t1.CUSIP = t2.CUSIP AND t1.quantity = t2.quantity
WHERE t1.clientName <> 'WFS'
AND t1.CUSIP IN (
    SELECT CUSIP
    FROM Trace
    GROUP BY CUSIP
    ORDER BY SUM(quantity) DESC 
)
ORDER BY margin DESC limit 4;
""";
    # Initialize an instance of the Ollama model
    llm = Ollama(model="sqlcoder",temperature=0)
    llm2 = Ollama(model="llama3")

    prompt = f""" 
    ### Instructions:
    Forget everything before and treat this as a fresh new schema
    Your task is to convert a question into a SQL query, given a MySQL database schema. Note Carefully that the DB is MySQL, so the query generated should be MySql Querry format
    Adhere to these rules:
    - **Deliberately go through the question and database schema word by word** to appropriately answer the question
    - **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
    - output should be an MySQL query, it should not be containing NULLS LAST phrase like in Postgresql
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
    Just output the sql querry:
    ```sql"""

    # Invoke the model to generate responses
    modelResponse = llm2.invoke(prompt)

    modelResponse = llm2.invoke("From the following string give just an proper mysql querry,Note do not write anything else in the response except for the sql querry. Note make changes to the querry so that it becomes a proper mysql querry: "+modelResponse)


    print(f"SQL Querry: {modelResponse}\n\n")
    return modelResponse
    #return "SELECT s.stockname, s.changes FROM stockmarket s ORDER BY s.changes DESC LIMIT 10;"

def executeQuery(querySQL):
        # Create a connection to the database
    db = mysql.connector.connect(
    host="localhost",  # replace with your host name
    user="root",  # replace with your username
    password="pass",  # replace with your password
    database="coporate_bonds"  # replace with your database name
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
    st.set_page_config(page_title="Lumen.AI")
    st.header("Lumen.AI")
    # Create a text input box and get the user input
 
    user_input = st.text_input("Enter your input here:")

    if user_input:
        with st.spinner('Processing...'):
            with st.expander("Generating SQL Query based on your input",expanded=True):
                modelGenQuery = llmForSQL(user_input)
                st.write(modelGenQuery)
            
            st.write("Executing the Query in the DB")
            df = executeQuery(modelGenQuery)

            with st.expander("Response From DB",expanded=True):
                st.write(df)

            st.write("Plotting the Data")
            with st.expander("Plot",expanded=True):
                fig = plotAI(df) 
                st.image(fig)
                #st.image("C:/Users/bjarj/OneDrive/Documents/GitHub/LLM-Poc/exports/charts/temp_chart.png")
            

def plotAI(df):
    llm = Ollama(model="llama3")
    df = SmartDataframe(df, config={"llm": llm})
    plot = df.chat("Plot margin as bar graph. give x axis the CUSIP and y axis as Margin. Give title 'Margin of missed trades'")
    
    # Return the absolute path of the file
    return plot


if __name__ == "__main__":
    main()