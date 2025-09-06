
# AtliQ Tees: Talk to a Database  


This is an end-to-end LLM project based on Google Gemini (Generative AI) and LangChain. We are building a system that can talk to a MySQL database.
Users ask questions in natural language, and the system generates answers by converting those questions to SQL queries and executing them on the MySQL database.
AtliQ Tees is a T-shirt store where inventory, sales, and discounts data are maintained in MySQL. A store manager may ask questions such as:
- How many white color Adidas t-shirts do we have left in stock?
- How much sales will our store generate if we sell all extra-small size t-shirts after applying discounts?
The system is intelligent enough to generate accurate queries for a given question and execute them on the MySQL database.

![](atliq_tees.png)

## Project Highlights

- AtliQ Tees is a t shirt store that sells Adidas, Nike, Van Heusen and Levi's t shirts 
- Their inventory, sales and discounts data is stored in a MySQL database
- We will build an LLM based question and answer system that will use following,
  - Google Gemini LLM (via Google Generative AI)
  - Hugging Face embeddings
  - Streamlit for UI
  - LangChain framework (v0.2+ with new community imports)
  - ChromaDB as a vector store
  - Few-shot learning
- In the UI, store manager will ask questions in a natural language and it will produce the answers


## Installation

1.Clone this repository to your local machine using:

```bash
  git clone https://github.com/codebasics/langchain.git
```
2.Navigate to the project directory:

```bash
  cd 4_sqldb_tshirts
```
3. Install the required dependencies using pip (includes cryptography for MySQL auth):

```bash
  pip install -r requirements.txt
```
4. Acquire an API key through makersuite.google.com and put it in a `.env` file

```bash
  GOOGLE_API_KEY="your_api_key_here"
```
5. For database setup, run `database/db_creation_atliq_t_shirts.sql` in your MySQL workbench

## Usage

1. Run the Streamlit app by executing:
```bash
streamlit run main.py

```

2. The web app will open in your browser where you can ask questions.

## Sample Questions
  - How many total t-shirts are left in stock?
  - How many t-shirts do we have left for Nike in XS size and white color?
  - How much is the total price of the inventory for all S-size t-shirts?
  - How much sales amount will be generated if we sell all small size Adidas shirts today after discounts?
  
## Project Structure

- main.py: The main Streamlit application script.
- langchain_helper.py: Contains all LangChain logic, including:
  - Updated imports for LangChain v0.2+ (using `langchain_community`)
  - Uses Google Gemini LLM via `langchain_google_genai`
  - Returns scalar results (e.g., 135 instead of [(Decimal('135'),)])
  - Handles prompt and SQL formatting to avoid syntax errors
- requirements.txt: A list of required Python packages for the project.
- few_shots.py: Contains few-shot prompt examples (ensure SQL queries do not start with 'sql' or 'SQLQuery:')
- .env: Configuration file for storing your Google API key.
## Notes

- Make sure your few-shot SQL examples and prompt templates do not include extra keywords like `sql` or `SQLQuery:` before the actual SQL statement. Queries should start directly with `SELECT ...`.
- The system now returns clean scalar results for aggregate queries (e.g., just `135` instead of `[(Decimal('135'),)]`).
- All deprecated LangChain imports have been updated to use the new `langchain_community` modules.
- The `cryptography` package is required for MySQL authentication and is included in requirements.