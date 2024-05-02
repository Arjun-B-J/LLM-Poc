import os
os.environ['HF_HOME'] = 'D:\\llm\\cache'
os.environ['TRANSFORMERS_CACHE'] = 'D:\\llm\\cache'
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

load_dotenv(find_dotenv())

#sql 
def sql():
    generator = pipeline("text-generation", model="codellama/CodeLlama-7b-hf")

    prompt = "This is my Database schema, CREATE TABLE Student (student_id INT PRIMARY KEY AUTO_INCREMENT,first_name VARCHAR(255) NOT NULL,last_name VARCHAR(255) NOT NULL,date_of_birth DATE,email VARCHAR(255) UNIQUE,phone_number VARCHAR(20),grade_level INT,major_id INT,FOREIGN KEY (major_id) REFERENCES Major(major_id));Retrieve the total number of student names which starts with letter A."

    # Generate the SQL query
    result = generator(prompt, max_length=1000, do_sample=True, temperature=0.7)

    # Extract the generated SQL query
    generated_query = result[0]['generated_text']
    
    print(result)

sql()