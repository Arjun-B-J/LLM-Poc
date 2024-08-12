import streamlit as st
from langchain_community.llms import Ollama
import mysql.connector
import pandas as pd
from pandasai import SmartDataframe
import os

def llmForSQL(query):
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
    modelResponse = llm.invoke(prompt)

    modelResponse = llm2.invoke("From the following string give just an proper mysql querry,Note do not write anything else in the response except for the sql querry. Note make changes to the querry so that it becomes a proper mysql querry: "+modelResponse)


    print(f"SQL Querry: {modelResponse}\n\n")
    return modelResponse

def executeQuery(querySQL):
        # Create a connection to the database
    db = mysql.connector.connect(
    host="localhost",  # replace with your host name
    user="root",  # replace with your username
    password="pass",  # replace with your password
    database="creditcard"  # replace with your database name
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

    # Initialize session state to store query history
    if 'query_history' not in st.session_state:
        st.session_state['query_history'] = []

    query_container = st.container()

    with query_container:
        user_input = st.text_input("Enter your Query here:")

    if user_input:
        with st.spinner('Processing...'):
            modelGenQuery = llmForSQL(user_input)  # Assume llmForSQL is a function that generates SQL query
            df = executeQuery(modelGenQuery)  # Assume executeQuery is a function that executes the SQL query and returns a dataframe

            # Store the query and result in the session state history
            st.session_state['query_history'].append((user_input, modelGenQuery, df))

    # Display previous queries and results in reverse order
    for idx, (user_query, sql_query, result) in enumerate(reversed(st.session_state['query_history'])):
        with st.expander(f"{len(st.session_state['query_history']) - idx}: {user_query}", expanded=True):
            st.markdown(f"**User Input:** {user_query}")
            st.markdown(f"**Generated SQL Query:**\n```sql\n{sql_query}\n```")
            st.markdown("**Response From DB:**")
            st.write(result)

            # Plotting the data
            st.markdown("**Plotting the Data**")
            # Add your plotting logic here. For demonstration, using a sample image.
            st.image("C:/Users/bjarj/OneDrive/Documents/GitHub/LLM-Poc/exports/charts/temp_chart.png")





def plotAI(df):
    llm = Ollama(model="llama3")
    df = SmartDataframe(df, config={"llm": llm})
    plot = df.chat("Plot as a bar graph, give y axis Customer Count and mark X axis with the city names from the data, give appropriate titles'")
    
    # Return the absolute path of the file
    return plot


if __name__ == "__main__":
    main()
