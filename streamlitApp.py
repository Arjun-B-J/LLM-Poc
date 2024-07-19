import streamlit as st
from langchain_community.llms import Ollama
import mysql.connector
import pandas as pd
from pandasai import SmartDataframe
import os

def llmForSQL(query):
    return """SELECT CITY, COUNT(*) AS CustomerCount
FROM Customer
WHERE DATEDIFF(CURRENT_DATE, LASTPAYMENT) >= 99 
  AND LASTCONTACT = CURRENT_DATE 
  AND ADJUSTLIMIT = TRUE
GROUP BY CITY;
"""
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
    #return "SELECT s.stockname, s.changes FROM stockmarket s ORDER BY s.changes DESC LIMIT 10;"

def executeQuery(querySQL):
        # Create a connection to the database
    db = mysql.connector.connect(
    host="localhost",  # replace with your host name
    user="root",  # replace with your username
    password="pass",  # replace with your password
    database="coporate_bondsv2"  # replace with your database name
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


import streamlit as st

def main():
    st.set_page_config(page_title="Lumen.AI", layout="centered")
    st.header("Lumen.AI")

    # Initialize session state to store query history
    if 'query_history' not in st.session_state:
        st.session_state['query_history'] = []
    if 'query_index' not in st.session_state:
        st.session_state['query_index'] = 0

    queries = [
        {
            "query": """SELECT cusip,
       Sum(quantity) AS quantity
FROM   trace
GROUP  BY cusip
ORDER  BY quantity DESC
LIMIT  5; """,
            "imgLoc": "tempPlots/1.png"
        },
        {
            "query": """SELECT s.cusip,
       s.ticker
FROM   security s
       INNER JOIN trace t
               ON t.cusip = s.cusip
WHERE  dealer <> 'WFS'
       AND s.cusip NOT IN (SELECT cusip
                           FROM   trades); """,
            "imgLoc": ""
        },
        {
            "query": """SELECT t1.cusip,
       s.ticker,
       ( t1.price - t2.price ) AS margin,
       t2.dealer
FROM   trades t1
       INNER JOIN security s
               ON t1.cusip = s.cusip
       LEFT JOIN trace t2
              ON t2.cusip = s.cusip
WHERE  t2.dealer <> 'WFS'
       AND s.cusip IN (SELECT cusip
                       FROM   top5tradedbonds)
ORDER  BY margin DESC; """,
            "imgLoc": "tempPlots/2.png"
        },
        {
            "query": """SELECT t1.cusip,
       s.ticker,
       o.quantity,
       o.active
FROM   trades t1
       INNER JOIN security s
               ON t1.cusip = s.cusip
       LEFT JOIN trace t2
              ON t2.cusip = s.cusip
       INNER JOIN offers o
               ON o.cusip = s.cusip
WHERE  t2.dealer <> 'WFS'
       AND active = 1
       AND s.cusip IN (SELECT cusip
                       FROM   top5tradedbonds); """,
            "imgLoc": ""
        },{
            "query": """SELECT s.cusip,
       s.ticker,
       o.quantity AS supply,
       t.quantity AS demand,
       o.active
FROM   security s
       INNER JOIN offers o
               ON s.cusip = o.cusip
       INNER JOIN trace t
               ON t.cusip = s.cusip
WHERE  active = 1; """,
            "imgLoc": "tempPlots/3.png"
        },{
            "query": """SELECT s.cusip,
       s.ticker,
       o.quantity AS supply,
       t.quantity AS demand,
       o.active
FROM   security s
       INNER JOIN offers o
               ON s.cusip = o.cusip
       INNER JOIN trace t
               ON t.cusip = s.cusip
WHERE  active = 1; """,
            "imgLoc": "tempPlots/4.png"
        }
    ]

    query_container = st.container()

    with query_container:
        user_input = st.text_area("Enter your Query here:", height=50, key="user_input")
        st.markdown("""
            <style>
            .stTextArea textarea {
                width: calc(100% - 40px) !important;
                padding-right: 40px !important;
                padding-bottom: 40px !important;
            }
            .stTextArea:after {
                content: '\\1F399'; /* Unicode character for microphone icon */
                font-size: 24px;
                position: absolute;
                right: 10px;
                bottom: 10px;
                cursor: pointer;
            }
            [data-testid="InputInstructions"] { display: none; }
            </style>
            """, unsafe_allow_html=True)

    if user_input:
        with st.spinner('Processing...'):
            current_query = queries[st.session_state['query_index']]['query']
            current_imgLoc = queries[st.session_state['query_index']]['imgLoc']

            df = executeQuery(current_query)  # Assume executeQuery is a function that executes the SQL query and returns a dataframe

            # Store the query and result in the session state history
            st.session_state['query_history'].append((user_input, current_query, df, current_imgLoc))

            # Update the index to fetch the next query in the next input
            st.session_state['query_index'] = (st.session_state['query_index'] + 1) % len(queries)

    # Display previous queries and results in reverse order
    for idx, (user_query, sql_query, result, imgLoc) in enumerate(reversed(st.session_state['query_history'])):
        with st.expander(f"{len(st.session_state['query_history']) - idx}: {user_query}", expanded=True):
            st.markdown(f"**Generated SQL Query:**\n```sql\n{sql_query}\n```")
            st.markdown("**Response From DB:**")
            st.write(result)

            # Plotting the data
            if(imgLoc!=""):
                st.markdown("**Plotting the Data**")
                st.image(imgLoc)



def plotAI(df):
    llm = Ollama(model="llama3")
    df = SmartDataframe(df, config={"llm": llm})
    plot = df.chat("Plot as a bar graph, give y axis Customer Count and mark X axis with the city names from the data, give appropriate titles'")
    
    # Return the absolute path of the file
    return plot


if __name__ == "__main__":
    main()