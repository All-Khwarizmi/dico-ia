from os import system
from h11 import CLIENT
import streamlit as st
from ui_text import *
from utils import *
import pandas as pd
from prompts import *
from openai import OpenAI

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
model_list = ["mistralai/mistral-7b-instruct", "nousresearch/nous-capybara-7b"]
MODE_NAME = "mistralai/mistral-7b-instruct"


st.title(TITLE)
st.subheader(MAIN_TITLE_SUBHEADER)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
     
# Try to initialize the files (for keeping track of prompt design and logging)
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
    response = llm_call(TRANSLATION_SYSTEM_PROMPT, word_to_translate, MODE_NAME)
    
    # Check if the prompt is already in the system prompts file
    translate_system_prompt_id = check_and_add_system_prompt(translation_direction)
    
    # Add interaction to interactions file
    add_llm_call_row(translate_system_prompt_id, "translate_call", word_to_translate, response.choices[0].message.content, MODE_NAME )
    
    # Display the translation
    st.success(response.choices[0].message.content)


         
# Importing the dataset 
df = pd.read_csv('interactions.csv')

# Displaying the dataset as a table
st.sidebar.subheader('Tableau des interactions')
st.sidebar.dataframe(df)

# Check if dataset is empty and if not, show possiblity of adding a quality  and comments
if not df.empty:
    st.sidebar.subheader('Ajouter une qualité et des commentaires')
    quality = st.sidebar.selectbox('Qualité', ['','1', '2', '3', '4', '5'])
    comments = st.sidebar.text_input('Commentaires')
    if st.sidebar.button('Ajouter'):
        update_last_row_quality_comments(quality, comments)
        st.sidebar.success("Qualité et commentaires ajoutés avec succès!")

# Add sidebar Q&A to tell users in french how to use the app and why thre're certain constraints
st.sidebar.title(SIDEBAR_TITLE)
st.sidebar.markdown(SIDEBAR_SUBHEADER_1)
st.sidebar.markdown(QANDA_1)
st.sidebar.markdown(QANDA_2_QUESTION)
st.sidebar.markdown(QANDA_2_ANSWER)
st.sidebar.markdown(QANDA_3_QUESTION)
st.sidebar.markdown(QANDA_3_ANSWER)



