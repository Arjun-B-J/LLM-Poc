from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

load_dotenv(find_dotenv())

# img2txt

def img2txt(url):
    image_to_text = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
    text = image_to_text(url)
    print(text)

#sql 
def sql():
    pipe = pipeline("text-generation", model="defog/sqlcoder2")

    prompt = "This is my Database schema, CREATE TABLE Student (student_id INT PRIMARY KEY AUTO_INCREMENT,first_name VARCHAR(255) NOT NULL,last_name VARCHAR(255) NOT NULL,date_of_birth DATE,email VARCHAR(255) UNIQUE,phone_number VARCHAR(20),grade_level INT,major_id INT,FOREIGN KEY (major_id) REFERENCES Major(major_id));Retrieve the total number of student names which starts with letter A."

    # Generate SQL query
    sql_query = pipe(prompt)[0]["generated_text"]
    print(f"Generated SQL query: {sql_query}")

    print(f"Generated SQL query: {sql_query}")

#img2txt("img.jpg")
sql()