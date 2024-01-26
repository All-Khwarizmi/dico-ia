import csv
import os
import datetime
from openai import OpenAI
import streamlit as st
from prompts import *
import pandas  as pd

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
CLIENT = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
) 

# File paths
system_prompts_file = 'system_prompts.csv'
interactions_file = 'interactions.csv'

# Initialize files with headers
def init_files():
    if not os.path.exists(system_prompts_file):
        with open(system_prompts_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['PromptID', 'SystemPrompt'])

    if not os.path.exists(interactions_file):
        with open(interactions_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['UserPrompt', 'SystemPromptID', 'PromptName', 'LLMResponse', 'ModelName', 'Date', 'Quality', 'Comments', 'UserFeedback', ])

# Function to add a new system prompt
def add_system_prompt(prompt):
    prompt_id = 1
    prompts = {}

    if os.path.exists(system_prompts_file):
        with open(system_prompts_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                prompts[row['SystemPrompt']] = row['PromptID']
                prompt_id = max(prompt_id, int(row['PromptID']) + 1)
        print("Added system prompt with ID:", prompt_id)
            

    if prompt not in prompts:
        with open(system_prompts_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([prompt_id, prompt])
        prompts[prompt] = prompt_id
        print("Added system prompt:", prompt)

    return prompts[prompt]

# Function to get the ID of a system prompt
def get_system_prompt_id(prompt):
    with open(system_prompts_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['SystemPrompt'] == prompt:
                return row['PromptID']
    return None

# Function to log an interaction with LLM
def add_llm_call_row(system_prompt_id,prompt_name, user_prompt, llm_response, model_name, quality=None, comments=None, user_feedback=None):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(interactions_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_prompt, system_prompt_id,prompt_name, llm_response, model_name, date_time, quality, comments, user_feedback, ])


# Function to update quality and comments for the last row
def update_last_row_quality_comments(quality, comments):
    if not os.path.exists(interactions_file):
        print("Interactions file does not exist.")
        return

    with open(interactions_file, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) > 1:  # Check if there's more than just the header
        rows[-1][5] = quality   # Update quality
        rows[-1][6] = comments  # Update comments

        with open(interactions_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    else:
        print("No interaction data to update.")

# Function to check if a prompt is in the system prompts file and store it if not
def check_and_add_system_prompt(prompt):
    system_prompt_id = get_system_prompt_id(prompt)
    if system_prompt_id is None:
        system_prompt_id = add_system_prompt(prompt)
    return system_prompt_id   

# A wrapper function of the LLM call 
def llm_call(system_prompt, user_prompt, model_name):
    response = CLIENT.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt} 
        ],
    stream=False,
    )

    return response    

# A llm_call like function that only takes a system prompt and a model name
def llm_call_2(system_prompt, model_name):
    response = CLIENT.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "user", "content": system_prompt} 
        ],
    stream=False,
    )

    return response

# Function that takes a prompt coming from the user, split it into words, counts the number of words and returns true if the number of words that are more than 3 characters long are less than 3, false otherwise
def get_words_less_than_3_chars(prompt):
    words = prompt.split()
    count = 0
    for word in words:
        if len(word) > 3:
            count += 1
    return count < 3

# Function that takes a translation direction ie "Français - Espagnol" and a word and inserts it into a system prompt according to the template
def get_translation_system_prompt(translation_direction, word):
    return SYSTEM_PROMPTS[translation_direction].replace("TARGET", word)

TRADUCTIONS = [
    "Français - Espagnol",
    "Français - Anglais",
    "Français - Allemand",
    "Espagnol - Français",
    "Anglais - Français",
    "Allemand - Français",
]


def sidebar_prompt_monitoring(ENV):
    if ENV == "dev":
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