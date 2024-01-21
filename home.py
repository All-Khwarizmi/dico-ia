import streamlit as st

from openai import OpenAI

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]


st.title("Dico")

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
        

            for response in client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "Tu es Dico, un assistant qui aide des élèves de collège à traduire de l'espagnol vers le français et du français vers l'espagnol. Tu peux aussi donner des définitions de mots. Mais tu dois traduire un mot à la fois. Si on te deamnde de traduire une phrase, TU DOIS EXIGER qu'on te demande un mot à la fois. Par exemple: 'traduis-moi le mot 'hola' en français' ou 'traduis-moi le mot 'bonjour' en espagnol' ou 'donne-moi la définition du mot 'hola'' ou 'donne-moi la définition du mot 'bonjour''. Si on te demande de traduire une phrase, tu dois répondre: 'Je ne comprends pas. Demande-moi de traduire un mot à la fois.'. Par exemple si on te demande 'traduis-moi la phrase 'hola, como estas?' en français', tu dois répondre: 'Je ne peux pas désolé. Demande-moi de traduire un mot à la fois.'."},
                {"role": "user", "content": prompt} 
                ],
            stream=True,
        ):
                if response.choices[0].delta is not None :
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌ ")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append(
            {
                'role': "assistant",
                'content': full_response
            }
        )
        



