import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcq_generator.mcq_gen import generate_evaluate_chain
from src.mcq_generator.logger import logging

# loading the response json file
with open("src/mcq_generator/response_json.json", "r") as f:
    response_json = json.load(f)

# creating the title of the app
st.title("Multiple Choice Quiz Generator")

# creating a form for all inputs
with st.form(key="mcq_generator_form"):
    # uploading the file
    uploading_file = st.file_uploader("Upload your file", type=["PDF","txt"])

    mcq_count = st.number_input("How many MCQs do you want to generate?", min_value= 3,max_value=30)

    subject = st.text_input("Enter the subject you want to generate MCQs for")

    tone = st.text_input("Enter the tone you want to generate MCQs for",placeholder="Easy")

    button = st.form_submit_button("Generate MCQs")

    # procced to generate after clicking on the button
    if button and uploading_file is not None:
        try:
            # generating the MCQs
            with st.spinner("Generating MCQs..."):
                text = read_file(uploading_file)

                with get_openai_callback() as callback:
                    response = generate_evaluate_chain(
                        {"text":text, 
                         "number":mcq_count, 
                         "subject":subject, 
                         "tone":tone, 
                         "response_json": json.dumps(response_json)
                        })
                    st.write("MCQs generated successfully")

            generate_evaluate_chain(uploading_file, mcq_count, subject, tone, response_json)
            st.write("MCQs generated successfully")
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error(f"Error generating the MCQs: {e}") 

        else:
            print(f"Total tokens generated: {callback.total_tokens}")
            print(f"Prompt Tokens generated: {callback.prompt_tokens}")
            print(f"Completed tokens generated: {callback.completed_tokens}")
            print(f"Total cost: {callback.total_cost}")

            if isinstance(response, dict):
                # extract the generated MCQs
                mcqs = response.get["quiz",None]
                if mcqs is not None:
                    table_data = get_table_data(mcqs)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index+1
                        st.table(df)
                        # Also display the review
                        st.text_area('review', value=response.get["review"])

                    else:
                        st.error("Error in creating table data")

            else:
                st.write(response)