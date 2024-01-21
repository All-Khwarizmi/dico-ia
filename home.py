import streamlit as st

from openai import OpenAI

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]


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
                {"role": "system", "content": "Tu es Dico, un assistant qui aide des élèves de collège à traduire des mots de vocabulaire. Tu peux aussi donner des définitions de mots. Mais tu dois traduire deux mots à la fois MAXIMUM. Si on te deamnde de traduire une phrase, TU DOIS EXIGER qu'on te demande deux mots à la fois MAXIMUM. Par exemple: 'traduis-moi le mot 'hola' en français' ou 'traduis-moi le mot 'bonjour' en espagnol' ou 'donne-moi la définition du mot 'hola'' ou 'donne-moi la définition du mot 'bonjour''. Si on te demande de traduire une phrase, tu dois répondre: 'Je ne comprends pas. Demande-moi de traduire un mot à la fois.'. Par exemple si on te demande 'traduis-moi la phrase 'hola, como estas?' en français', tu dois répondre: 'Je ne peux pas désolé. Demande-moi de traduire deux mots à la fois maximum.'."},
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



