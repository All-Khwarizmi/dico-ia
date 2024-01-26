from os import system
import streamlit as st
from utils import add_system_prompt, get_system_prompt_id, add_llm_call_row, init_files, update_last_row_quality_comments
import pandas as pd
from prompts import *
from openai import OpenAI

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
model_list = ["mistralai/mistral-7b-instruct", "nousresearch/nous-capybara-7b"]
MODE_NAME = "mistralai/mistral-7b-instruct"


st.title("DicoIA")
st.subheader("Un assistant qui aide des élèves de collège à traduire des mots de vocabulaire et à donner des définitions de mots.")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
) 

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
     
# Try to initialize the files (for keeping track of prompt design and logging)
try:
    init_files()
except:
    st.error("Error initializing files. Please check the file permissions.")
prompt = st.chat_input("Que veux-tu savoir ?")
if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
             st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Ask LLM to extract the words that the user wants to translate
           
            response = client.chat.completions.create(
            model=MODE_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_3},
                {"role": "user", "content": prompt} 
                ],
            stream=False,
            )
            # Check if the prompt is already in the system prompts file
            system_prompt_id = get_system_prompt_id(SYSTEM_PROMPT_3)
            if system_prompt_id is None:
                # Add prompt to system prompts file
                system_prompt_id = add_system_prompt(SYSTEM_PROMPT_3)
            
            # Add interaction to interactions file
            add_llm_call_row(system_prompt_id, "extract_words_call", prompt, response.choices[0].message.content, MODE_NAME )
            

            # Ask LLM if promt is complaint with the length constraint. If not, ask user to rephrase. Indeed, the LLM is trained to translate only two words at a time.
            print("prompt: ", prompt)
            
            response = client.chat.completions.create(
            model=MODE_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt} 
                ],
            stream=False,    
            )
            
            # Check if the prompt is already in the system prompts file
            system_prompt_id = get_system_prompt_id(SYSTEM_PROMPT)
            if system_prompt_id is None:
                # Add prompt to system prompts file
                system_prompt_id = add_system_prompt(SYSTEM_PROMPT)
                
            # Add interaction to interactions file
            add_llm_call_row(system_prompt_id, "is_compliant_call", prompt, response.choices[0].message.content, MODE_NAME )            
           
            # Check if user prompt is compliant with the length constraint. Check if response contains "OUI" or "NON"
            if "OUI" in response.choices[0].message.content:
                print("OUI")
                print(response.choices[0])
                
                for response in client.chat.completions.create(
                model="nousresearch/nous-capybara-7b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_2},
                    {"role": "user", "content": prompt} 
                    ],
                    stream=True,
                ):
                    if response.choices[0].delta is not None :
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌ ")
                message_placeholder.markdown(full_response)
            else:
                print("NON")
                print(response.choices)
                message_placeholder.markdown("""
                Je ne peux traduire une phrase. Demande-moi de traduire un mot à la fois MAXIMUM.
                """)
                full_response = """
                Je ne peux traduire une phrase. Demande-moi de traduire un mot à la fois MAXIMUM.
                """
                st.session_state.messages.append(
                    {
                        'role': "assistant",
                        'content': full_response
                    }
                )
            
                
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
st.sidebar.title("Q&A")
st.sidebar.markdown("### Comment utiliser DicoIA?")
st.sidebar.markdown("DicoIA est un assistant qui aide des élèves de collège à traduire des mots de vocabulaire et à donner des définitions de mots. Mais il y a certaines contraintes. DicoIA ne peut traduire que deux mots à la fois MAXIMUM. ")
st.sidebar.markdown("### Pourquoi DicoIA ne peut traduire que deux mots à la fois MAXIMUM?")
st.sidebar.markdown("Parce que DicoIA est un assistant qui aide des élèves de collège à traduire des mots, à donner des définitions de mots et à apprendre des mots de vocabulaire. Mais plus important encore, il est conçu pour éduquer les élèves à utiliser un traducteur judicieusement et développer leur autonomie.")
st.sidebar.markdown("### Comment formuler une question à DicoIA?")
st.sidebar.markdown("Pour formuler une question à DicoIA, il faut dire: 'traduis-moi le mot 'hola' en français' ou 'traduis-moi le mot 'bonjour' en espagnol' ou 'donne-moi la définition du mot 'hola'' ou 'donne-moi la définition du mot 'bonjour'.")
st.sidebar.markdown("### Pourquoi les guillemets (\"\") sont-ils nécessaires?")
st.sidebar.markdown("Les guillemets (\"\") sont nécessaires pour aider DicoIA à déterminer quels mots traduire.")

# Questions et conseils méthodologiques pour développer l'autonomie des élèves et les aider à utiliser un traducteur judicieusement
st.sidebar.markdown("### Comment je fais si j'ai besoin de traduire une phrase?")
st.sidebar.markdown("Pour construire une phrase tu dois d'abord réfléchir à ce que tu veux dire. Ensuite, tu dois essayer de trouver les mots qui te permettent de dire ce que tu veux dire. Tu peux te servir du matériel de cours à ta disposition. Fais des phrases simples. ")


