import streamlit as st
from ui_text import *
from utils import *
import pandas as pd
from prompts import *


st.set_page_config(
    page_title=TITLE,
    page_icon="🐙",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title(TITLE)
st.subheader(MAIN_TITLE_SUBHEADER)
st.divider()

# Initialize dataframe in state to store user translations
if "TRANSLATIONS" not in st.session_state:
    st.session_state["TRANSLATIONS"] = pd.DataFrame(columns=["Direction", "Word", "Translation"])
     
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
    word_to_translate_format = get_translation_system_prompt(translation_direction, word_to_translate)
    PROMPT = get_translation_system_prompt_target(translation_direction)
    response = llm_call(PROMPT, word_to_translate, MODEL_NAME)
    
    # Check if the prompt is already in the system prompts file
    translate_system_prompt_id = check_and_add_system_prompt(PROMPT)
    
    # Add interaction to interactions file
    add_llm_call_row(translate_system_prompt_id, "translate_call", word_to_translate, response.choices[0].message.content, MODEL_NAME )
    
    # Display the translation
    st.success(response.choices[0].message.content)

    
    # Add the translation to the chat history
    st.session_state["TRANSLATIONS"].loc[len(st.session_state["TRANSLATIONS"])] = [translation_direction, word_to_translate, response.choices[0].message.content]   
        
    

# Display the translations history
if not st.session_state["TRANSLATIONS"].empty:
    st.divider()
    st.subheader("Historique des traductions")
    st.dataframe(st.session_state["TRANSLATIONS"])    

sidebar_prompt_monitoring(ENV)
# Add sidebar Q&A to tell users in french how to use the app and why thre're certain constraints
sidebar_QA(st)



