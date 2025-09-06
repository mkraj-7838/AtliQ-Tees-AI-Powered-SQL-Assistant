import streamlit as st
import re  # Import the regular expression module
from langchain_helper import get_few_shot_db_chain

st.title("AtliQ T-Shirts: Database Q&A 👕")

question = st.text_input("Question:", placeholder="e.g., How many white Nike shirts do we have?")

if question:
    try:
        chain = get_few_shot_db_chain()
        with st.spinner("Generating SQL and querying the database..."):
            response = chain.invoke({"query": question})
        
        raw_result = response["result"]

        # --- CORRECTED CODE BLOCK ---
        # Use a regular expression to find the number inside "Decimal('...')".
        # This is more robust than ast.literal_eval for this specific format.
        match = re.search(r"Decimal\('(\d+)'\)", raw_result)
        
        if match:
            # If a match is found, extract the first captured group (the digits)
            # and convert it to an integer.
            value = int(match.group(1))
        else:
            # If the result is not in the Decimal format (e.g., a list of names),
            # display the raw result as a fallback.
            value = raw_result
        # --- END OF CORRECTION ---

        st.subheader("Answer")
        st.header(value)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Please ensure your database is running and the .env file is configured correctly.")