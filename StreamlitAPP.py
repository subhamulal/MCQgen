import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenrator.utils import read_file, get_table_data
from src.mcqgenrator.logger import logging
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback
from src.mcqgenrator.mcagenerator import generate_evaluate_chain


with open('C:/Users/HP/OneDrive/Desktop/MCQgen/Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Streamlit UI
st.title("MCQ Generation Application")

with st.form("user_input_form"):
    uploaded_file = st.file_uploader("Upload PDF or Text File")
    mcq_count = st.number_input("Number of Questions", min_value=3, max_value=50)
    subject = st.text_input("Enter Subject", max_chars=30, placeholder="Biology")
    tone = st.text_input("Complexity Level (e.g., simple)", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)

                # Define your chains before this block or import from module
                response = {}
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })

                    st.success("MCQs generated successfully.")
                    st.write(f"Total Tokens: {cb.total_tokens}")
                    st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                    st.write(f"Completion Tokens: {cb.completion_tokens}")
                    st.write(f"Total Cost (USD): ${cb.total_cost}")

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred during MCQ generation.")

            else:
                quiz = response.get("quiz")
                if quiz:
                    table_data = get_table_data(quiz)
                    if table_data:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)
                    else:
                        st.error("Error parsing quiz into table format.")
                else:
                    st.write("No quiz generated.")