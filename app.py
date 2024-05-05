import os
os.environ['HF_HOME'] = 'D:\\llm\\cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:\\llm\\cache'
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

load_dotenv(find_dotenv())

#sql 
def sql():
    generator = pipeline("text-generation", model="defog/sqlcoder2")

    prompt = """ 
### Instructions:
Your task is to convert a question into a SQL query, given a SQL database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float

### Input:
Generate a SQL query that answers the question `{Get all companies name starting with 'A' whose stock price OpenPrice is greaterthan 50}`.
This query will run on a database whose schema is represented in this string:
CREATE TABLE Companies (
    CompanyID INT PRIMARY KEY,
    Name VARCHAR(100),
    Industry VARCHAR(100),
    CEO VARCHAR(100),
    Headquarters VARCHAR(100),
    FoundedYear INT,
    Employees INT,
    MarketCap DECIMAL(15, 2),
    PE_Ratio DECIMAL(5, 2),
    DividendYield DECIMAL(5, 2),
    EPS DECIMAL(5, 2)
);

CREATE TABLE Stocks (
    StockID INT PRIMARY KEY,
    CompanyID INT,
    Date DATE,
    OpenPrice DECIMAL(10, 2),
    HighPrice DECIMAL(10, 2),
    LowPrice DECIMAL(10, 2),
    ClosePrice DECIMAL(10, 2),
    Volume BIGINT,
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);

CREATE TABLE Bonds (
    BondID INT PRIMARY KEY,
    CompanyID INT,
    IssueDate DATE,
    MaturityDate DATE,
    CouponRate DECIMAL(5, 2),
    FaceValue DECIMAL(10, 2),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);

CREATE TABLE Forex (
    ForexID INT PRIMARY KEY,
    BaseCurrency VARCHAR(10),
    QuoteCurrency VARCHAR(10),
    Date DATE,
    OpenRate DECIMAL(10, 5),
    HighRate DECIMAL(10, 5),
    LowRate DECIMAL(10, 5),
    CloseRate DECIMAL(10, 5)
);

CREATE TABLE Commodities (
    CommodityID INT PRIMARY KEY,
    CommodityName VARCHAR(50),
    Date DATE,
    OpenPrice DECIMAL(10, 2),
    HighPrice DECIMAL(10, 2),
    LowPrice DECIMAL(10, 2),
    ClosePrice DECIMAL(10, 2),
    Volume BIGINT
);

-- Stocks.CompanyID can be joined with Companies.CompanyID
-- Bonds.CompanyID can be joined with Companies.CompanyID

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{Get all companies name starting with 'A' whose stock price OpenPrice is greaterthan 50}`:
```sql
"""

    # Generate the SQL query
    result = generator(prompt, max_length=1000, do_sample=True, temperature=0.7)

    # Extract the generated SQL query
    generated_query = result[0]['generated_text']
    
    print(result)

sql()