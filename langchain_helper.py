# langchain_helper.py

import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from few_shots import few_shots

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain():
    # --- Database Connection ---
    db_user = "root"
    db_password = "Mkr%40j55905"
    db_host = "localhost"
    db_name = "atliq_tshirts"
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
        sample_rows_in_table_info=3
    )

    # --- LLM Configuration ---
    # FIX: Load API key securely from environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

    # FIX: Use a standard, valid model name like "gemini-pro"
    llm = GoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0.1
    )

    # --- Embeddings and Example Selector ---
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    # FIX: The vector store should be built from the Question-SQLQuery pairs
    to_vectorize = [f"Question: {e['Question']}\nSQLQuery: {e['SQLQuery']}" for e in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    # --- Prompt Engineering ---
    # FIX: The main prompt should only instruct the LLM to generate a query.
    # The chain will handle executing it and summarizing the result.
    mysql_prompt = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
Never query for all columns from a table. You must query only the columns that are needed to answer the question.
Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below.
Pay attention to use CURDATE() function to get the current date if the question involves "today".

"""

    # FIX: The example prompt should only contain Question and SQLQuery.
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\n",
    )

    # --- Few-Shot Prompt Template ---
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], # These are required by the SQLDatabaseChain
    )
    
    # --- Create and return the chain ---
    return SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt, return_direct=True)