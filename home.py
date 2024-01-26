import streamlit as st
from ui_text import *
from utils import *
import pandas as pd
from prompts import *

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
ENV = st.secrets["ENV"]
model_list = ["mistralai/mistral-7b-instruct", "nousresearch/nous-capybara-7b"]
MODEL_NAME = "mistralai/mistral-7b-instruct"


st.title(TITLE)
st.subheader(MAIN_TITLE_SUBHEADER)


     
# Try to initialize the files (for keeping track of prompt design monitoring and logging)
if ENV == "dev":
    try:
        init_files()
    except:
        st.error("Error initializing files. Please check the file permissions.")
         
# Streamlit selectbox to choose a translation direction (from language and to language)
translation_direction = st.selectbox('Choisis une direction de traduction', TRADUCTIONS)

# Streamlit text input to enter a word to translate
word_to_translate = st.text_input('Entre un mot à traduire')

# Streamlit button to trigger the translation
if st.button('Traduire'):
    # Check if the word to translate is not empty
    if word_to_translate == "":
        st.error("Entre un mot à traduire")
        st.stop()
    
    # Check if the word to translate is not more than 3 words
    get_words_less_than_3_chars(word_to_translate)
    if not get_words_less_than_3_chars(word_to_translate):
        st.error(MAX_LEN_ERROR_PLACEHOLDER)
        st.stop()
    
    # Call LLM to translate the word
    word_to_translate = get_translation_system_prompt(translation_direction, word_to_translate)
    response = llm_call(TRANSLATION_SYSTEM_PROMPT, word_to_translate, MODEL_NAME)
    
    # Check if the prompt is already in the system prompts file
    translate_system_prompt_id = check_and_add_system_prompt(translation_direction)
    
    # Add interaction to interactions file
    add_llm_call_row(translate_system_prompt_id, "translate_call", word_to_translate, response.choices[0].message.content, MODEL_NAME )
    
    # Display the translation
    st.success(response.choices[0].message.content)

    
    # Add the translation to the chat history
    

sidebar_prompt_monitoring(ENV)
# Add sidebar Q&A to tell users in french how to use the app and why thre're certain constraints
sidebar_QA(st)



