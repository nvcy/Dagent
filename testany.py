from sqlalchemy import create_engine, text
import psycopg2
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.schema import AgentSchema, JudgerSchema
from utils.DataBase import DataBase
from agents.Judge import JudgerAgent
from dotenv import load_dotenv
load_dotenv()
def engine_tester():
    """
    Tests the database connection and retrieves the list of tables in the 'dagent' schema.
    This function establishes a connection to the PostgreSQL database using SQLAlchemy and psycopg2.
    It then executes a query to fetch the names of all tables in the 'dagent'"""
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('HOST_PORT')}/{os.getenv('DATA_BASE')}"
    )

    with engine.connect() as connection:
        results = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema =:schema"), {'schema':'dagent'})
        tables = results.fetchall()
        print(f"Tables {tables[0]}")

# test Database utility class



def DBUtilityTester():
    """
    Tests the DataBase utility class by creating an instance and retrieving schema information.
    This function initializes the DataBase class with database configurations, retrieves schema information for the 'dagent' schema,
    and prints the schema details including table names, column names, data types, and sample data.
    """
    db_configs = {
        "USER": os.getenv('USER'),
        "PASSWORD": os.getenv('PASSWORD'),
        "HOST": os.getenv('HOST'),
        "HOST_PORT": os.getenv('HOST_PORT'),
        "DATA_BASE": os.getenv('DATA_BASE')
    }
    db = DataBase(db_configs)
    schema_info = db.SchemaIfo("dagent")
    with open("schema_info.txt", "w") as file:
        file.write(schema_info)
    print(f"\n\n\n\n +++++++++++Schema Info+++++++++++++++++: {schema_info}")


# tets gemini api 

def gemintester():
    """
    Tests the Gemini API by prompting the user for a topic and retrieving information about that topic in data engineering.
    This function initializes the ChatGoogleGenerativeAI model, creates a prompt template, and invokes
    the model with the user's input to generate a response."""
    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash",
                                 temperature=0.7, max_output_tokens=1024)
    prompt=ChatPromptTemplate.from_messages([
        ("system","you are expert in data engineering"),
        ("human", "what is Topic {topic} in data engineering?")
    ])
    chain = prompt | llm
    topic = input("Enter the topic you want to know about: ")
    response = chain.invoke({"topic": topic})
    print(response.content[0].get("text"))

def main():
    """
    Main function to execute the database connection test, DataBase utility test, and Gemini API test.
    This function sequentially calls the engine_tester, DBUtilityTester, and gemintester functions to perform their respective tests.
    """
    engine_tester()
    DBUtilityTester()
    gemintester()

#judger tester
def judger_tester():
    """
    Tests the JudgerSchema class by creating an instance and printing its attributes.
    This function initializes the JudgerSchema class with a sample SQL query, safety status, and comments,
    and then prints the values of its attributes to verify their correctness.
    """
    agentschema = AgentSchema(
        messages =["Hello, I have a question about the database."],
        user_question="SELECT * FROM dagent.users WHERE user_id = 1;",
        curated_question="SELECT * FROM dagent.users WHERE user_id = 1;",
        prompt_query_context="You are an intelligent database assistant specialized in SQL databases, database systems, and data engineering. Your task is to answer the user's question accurately using the provided database schema and your general technical knowledge. The following information describes the structure of the connected database: [Schema Info]. Provide the most relevant and accurate answer to the user's question.",
        is_safe="safe",
        generated_sql_query="SELECT * FROM dagent.users WHERE user_id = 1;",
        sql_query_results="[{'user_id': 1, 'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}]",
        final_response="The SQL query is safe and retrieves the user information for user_id 1."
    )
    judger = JudgerAgent(level="basic")
    response =judger.evaluate_sql_query(agentschema)
    print(f"SQL Query: {response.sql_query}")
    print(f"Is Safe: {response.is_safe}")
    print(f"Comments: {response.comments}")

if __name__ == "__main__":
    judger_tester()