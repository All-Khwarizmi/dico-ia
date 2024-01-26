

TITLE = "DicoIA"
MAIN_TITLE_SUBHEADER = "Un assistant qui aide des élèves de collège à traduire des mots de vocabulaire et à donner des définitions de mots."

MAX_LEN_ERROR_PLACEHOLDER = "Je ne peux traduire une phrase. Demande-moi de traduire un mot à la fois MAXIMUM."

SIDEBAR_TITLE = "Q&A"
SIDEBAR_SUBHEADER_1 = "### Comment utiliser DicoIA?"

QANDA_1 = "DicoIA est un assistant qui aide des élèves de collège à traduire des mots de vocabulaire et à donner des définitions de mots. Mais il y a certaines contraintes. DicoIA ne peut traduire que trois mots à la fois MAXIMUM. "

QANDA_2_QUESTION = "### Pourquoi DicoIA ne peut traduire que trois mots à la fois MAXIMUM?"

QANDA_2_ANSWER = "Parce que DicoIA est un assistant qui aide des élèves de collège à traduire des mots, à donner des définitions de mots et à apprendre des mots de vocabulaire. Mais plus important encore, il est conçu pour éduquer les élèves à utiliser un traducteur judicieusement et développer leur autonomie."

QANDA_3_QUESTION = "### Comment formuler une question à DicoIA?"

QANDA_3_ANSWER = """
Pour formuler une question à DicoIA, il faut dire:
1. Il faut choisir une direction de traduction dans la liste déroulante.
2. Il faut entrer un mot à traduire dans le champ de texte.
3. Il faut cliquer sur le bouton 'Traduire'.

"""
QANDA_4_QUESTION = "### Comment formuler une question à DicoIA pour avoir la définition d'un mot?"

# Conseil de méthode:
QANDA_5_QUESTION = "### Comment faire si j'ai besoin de plus d'informations?"
QANDA_5_ANSWER = """
Si tu as besoin de plus d'informations:
1. Prends le temps de réfléchir à ce que tu veux dire.
2. Formule ce que tu veux dire en utilisant des mots simples et phrases courtes.
3. Cherche à utiliser des mots que tu connais déjà. Regarde dans ton cahier, manuel ou autre ressource à ta disposition.
"""

# Function wrapper of the sidebar Q&A to tell users in french how to use the app and why thre're certain constraints
def sidebar_QA(st):
    st.sidebar.title(SIDEBAR_TITLE)
    st.sidebar.markdown(SIDEBAR_SUBHEADER_1)
    st.sidebar.markdown(QANDA_1)
    st.sidebar.markdown(QANDA_2_QUESTION)
    st.sidebar.markdown(QANDA_2_ANSWER)
    st.sidebar.markdown(QANDA_3_QUESTION)
    st.sidebar.markdown(QANDA_3_ANSWER)
    st.sidebar.markdown(QANDA_5_QUESTION)
    st.sidebar.markdown(QANDA_5_ANSWER)