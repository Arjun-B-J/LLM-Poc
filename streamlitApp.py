import re
import time
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




import streamlit as st

def executeQuery(querySQL):
        # Create a connection to the database
    db = mysql.connector.connect(
    host="localhost",  # replace with your host name
    user="root",  # replace with your username
    password="pass",  # replace with your password
    database="agileV2"  # replace with your database name
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
    st.set_page_config(page_title="Lumen.AI", layout="wide")

    # Remove top space using CSS
    st.markdown("""
        <style>
        /* Remove padding */
        .css-18e3th9, .css-1d391kg, .css-1v3fvcr {
            padding: 0rem;
        }
        /* Hide the "Deploy" button and the menu dots */
        header, footer, .viewerBadge_link__1S137 {
            display: none !important;
        }
        .reportview-container {
            margin-top: 0rem;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .st-emotion-cache-1jicfl2 {
            width: 100%;
            padding: 0rem 6rem 10rem;
            min-width: auto;
            max-width: initial;
        }
        .stTextArea textarea {
            font-size: 24px !important; /* Adjust the font size here */
        }               
        </style>
        """, unsafe_allow_html=True)

    st.header("Lumen.AI")

    # Initialize session state to store query history
    if 'query_history' not in st.session_state:
        st.session_state['query_history'] = []
    if 'query_index' not in st.session_state:
        st.session_state['query_index'] = 0

    queries = [
        {
            "query": """SELECT t.NAME,
       Round(Avg(s.pointssdelivered), 3)                  AS velocity,
       Round(Sum(s.pointssdelivered) / Sum(t.tmcount), 3) AS per_tm
FROM   team t
       INNER JOIN sprints s
               ON t.NAME = s.team
GROUP  BY t.NAME; """,
            "imgLoc": "charts/1.png"
        },
        {
            "query": """SELECT team,
       Count(*)         AS HowManyTimes,
       Avg(pointsadded) AS AveragePoints
FROM   sprints
WHERE  pointsadded > 0
       AND team IN (SELECT NAME
                    FROM   viewavgvelocity)
GROUP  BY team
ORDER  BY Count(*) DESC; """,
            "imgLoc": "charts/2.png"
        },
        {
            "query": """SELECT team,
       Count(*)         AS HowManyTimes,
       Sum(pointsadded) AS TotalPoints
FROM   sprints
WHERE  pointsadded > 0
       AND team IN (SELECT NAME
                    FROM   viewavgvelocity)
       AND pointscomitted > pointssdelivered
GROUP  BY team
ORDER  BY Count(*) DESC; """,
            "imgLoc": "charts/3.png"
        }
        ,
        {
            "query": """SELECT team,
       Count(*)         AS HowManyTimes,
       Sum(pointsadded) AS TotalPoints
FROM   sprints
WHERE  pointsadded > 0
       AND shrp > 0
       AND team IN (SELECT NAME
                    FROM   viewavgvelocity)
GROUP  BY team
ORDER  BY Count(*) DESC; """,
            "imgLoc": "charts/4.png"
        }
    ]

    


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

    query_container = st.empty()
    st.markdown(
    """
    <style>
    .streamlit-expanderHeader {
        font-size: 24px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    if user_input:
        with st.spinner('Processing...'):
            # Clear the query container before displaying new content
            query_container.empty()

            current_query = queries[st.session_state['query_index']]['query']
            current_imgLoc = queries[st.session_state['query_index']]['imgLoc']

            df = executeQuery(current_query)  # Assume executeQuery is a function that executes the SQL query and returns a dataframe

            # Store the query and result in the session state history
            st.session_state['query_history'].append((user_input, current_query, df, current_imgLoc))

            # Update the index to fetch the next query in the next input
            st.session_state['query_index'] = (st.session_state['query_index'] + 1) % len(queries)

            with query_container.container():
                with st.expander(f"Current Query: {user_input}", expanded=True):
                    cols = st.columns(2)
                    with cols[0]:
                        with st.spinner('Generating SQL Query...'):
                            sql_placeholder = st.empty()
                            full_query = ""
                            # Split by space or newline to keep the newlines intact
                            for word in re.split(r'(\s+|\n)', current_query):
                                full_query += word
                                sql_placeholder.markdown(f"**Generated SQL Query:**\n```sql\n{full_query}\n```")
                                time.sleep(0.04)
                            sql_placeholder.code(full_query.strip(), language='sql')
                    
                    with cols[1]:
                        with st.spinner('Getting Response from DB...'):
                            time.sleep(0.5)
                            st.markdown("**Response From DB:**")
                            st.write(df)

                    if current_imgLoc:
                        with st.spinner('Plotting the Data...'):
                            time.sleep(1)
                            st.markdown("**Plotting the Data**")
                            st.image(current_imgLoc, use_column_width='auto')
                    else:
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("\n\n\nVisualization Not Available\n\n\n")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")
                        st.markdown("   ")

    # Display previous queries and results in reverse order
    history_container = st.empty()
    with history_container.container():
        for idx, (user_query, sql_query, result, imgLoc) in enumerate(reversed(st.session_state['query_history'][:-1])):
            with st.expander(f"{len(st.session_state['query_history']) - 1 - idx}: {user_query}", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("**Generated SQL Query:**")
                    st.code(sql_query.strip(), language='sql')
                
                with cols[1]:
                    st.markdown("**Response From DB:**")
                    st.write(result)

                if imgLoc:
                    st.markdown("**Plotting the Data**")
                    st.image(imgLoc, use_column_width='auto')
                else:
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("\n\n\nVisualization Not Available\n\n\n")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
                    st.markdown("   ")
def plotAI(df):
    llm = Ollama(model="llama3")
    df = SmartDataframe(df, config={"llm": llm})
    plot = df.chat("Plot as a bar graph, give y axis Customer Count and mark X axis with the city names from the data, give appropriate titles'")
    
    # Return the absolute path of the file
    return plot


if __name__ == "__main__":
    main()