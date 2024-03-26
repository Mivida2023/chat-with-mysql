from dotenv import load_dotenv
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
import streamlit as st


load_dotenv()


def init_database(user: str, password: str, host: str, database: str) -> SQLDatabase:
  db_uri = f"postgresql://{user}:{password}@{host}/{database}"
  return SQLDatabase.from_uri(db_uri)

# Define the SQL chain
def get_sql_chain(db):
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
  
    Vous êtes un assistant expert en base de données compétent en SQL avec une compréhension approfondie des structures de table suivantes :
    
    <SCHEMA>{schema}</SCHEMA>

    Sur la base du schéma de la table et des questions de l'utilisateur à propos de la base de données de la société, vous écrivez des requêtes SQL appropriées. Écrivez uniquement la requête SQL et rien d'autre. N'encadrez pas la requête SQL dans un autre texte, pas même des backticks.
    
    Exemples :
    - Question : Quel est le montant total dépensé par John Doe dans ses commandes ?
      Requête SQL : SELECT SUM(prix) FROM commande JOIN contact ON commande.contact_id = contact.id WHERE contact.nom = 'Doe' AND contact.prenom = 'John';
    
    - Question : Lister tous les contacts qui ont passé une commande pour la France.
      Requête SQL : SELECT contact.nom, contact.prenom FROM contact JOIN commande ON contact.id = commande.contact_id WHERE commande.pays = 'France';
    
    - Question : Quelle est la note moyenne des commandes de John Doe ?
      Requête SQL : SELECT AVG(note) FROM avis JOIN commande ON avis_voyageur.commande_id = commande.id JOIN contact ON commande.contact_id = contact.id WHERE contact.nom = 'Doe' AND contact.prenom = 'John';
    
    - Question : Afficher tous les avis laissés par les clients sur les commandes pour la France.
      Requête SQL : SELECT contact.nom, contact.prenom, avis_voyageur.avis, avis.note FROM avis JOIN commande ON avis.commande_id = commande.id JOIN contact ON commande.contact_id = contact.id WHERE commande.pays = 'France';
    
    Historique des conversations : {chat_history}
    
    À votre tour :
    
    Question : {question}
    Requête SQL :
    """
    
  prompt = ChatPromptTemplate.from_template(template)
  
  llm = ChatOpenAI(model="gpt-4-0125-preview")
  # llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  #llm = ChatOllama(model="mistral:instruct")

  # Get the schema of the tables
  def get_schema(_):
    schema = db.get_table_info()
    print(schema)
    return schema
  
  return (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
  )

# Define the response chain to get the AI response  
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_chain = get_sql_chain(db)
  
  # Define the template for the chat prompt answer
  template = """
    Vous êtes un analyste de données chez le voyagiste français Voyages E.Leclerc. Vous interagissez avec un utilisateur qui vous pose des questions sur la base de données de l'entreprise.
    Sur la base du schéma de la table ci-dessous, de la question, de la requête SQL, et de la réponse SQL, rédigez une réponse en langage naturel.
    <SCHEMA>{schema}</SCHEMA>

    Historique des conversations : {chat_history}
    Requête SQL : <SQL>{query}</SQL>
    
    Question de l'utilisateur : {question}
    Réponse SQL : {response}

    Exemple:
    - Question de l'utilisateur : Combien a dépensé John Doe en total ?
    - Requête SQL : <SQL>SELECT SUM(prix) FROM commande JOIN contact ON commande.contact_id = contact.id WHERE contact.nom = 'Doe' AND contact.prenom = 'John';</SQL>
    - Réponse SQL : <RESPONSE>350</RESPONSE>
    - Réponse en Langage Naturel : John Doe a dépensé un total de 350 euros pour ses commandes.
      
    Utilisez les informations fournies pour formuler une réponse compréhensible et informative basée sur les résultats de la requête SQL en utilisant Markedown, des bulletpoint le cas échéant.
    Vous ne montrez aucune requete SQL dans votre réponse.
    
    À votre tour :
    
    Question: {question}
    SQL Query:
  """
  prompt = ChatPromptTemplate.from_template(template)
 
  llm = ChatOpenAI(model="gpt-4-0125-preview")
  # llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  # llm = ChatOllama(model="mistral:instruct")

  
  chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
      schema=lambda _: db.get_table_info(),
      response=lambda vars: db.run(vars["query"]),
    )
    | prompt
    | llm
    | StrOutputParser()
  )
  
  return chain.stream({
    "question": user_query,
    "chat_history": chat_history,
  })


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Salut! Je suis ton assistant Tip's VoIAge E.Leclerc. Demande moi ce que tu veux savoir sur la base de données."),
    ]

st.set_page_config(page_title="Chat avec Tip's de Voyage E.Leclerc",
                  page_icon=os.getenv('VEL_ICON'),
                  initial_sidebar_state="expanded")
with open("assets/style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



# Connect to database
with st.sidebar:
    st.image(os.getenv('VEL_LOGO'))
    st.header("Chat avec Tip's Voyage")
   
    with st.sidebar.expander("⚙️ Settings", expanded=True):
      st.subheader("Connectez-vous à la base de données et commencez vos recherches..")
      
      st.text_input("Host", value="localhost", key="Host")
      st.text_input("User", value="francois", key="User")
      st.text_input("Password", type="password", value="240365", key="Password")
      st.text_input("Database", value="bcu", key="Database")
      # Connect to database
      if st.button("Connect"):
          with st.spinner("Connection en cours..."):
              db = init_database(
                  st.session_state["User"],
                  st.session_state["Password"],
                  st.session_state["Host"],
                  st.session_state["Database"]
              )
              st.session_state.db = db
              st.success("Connecté à la base!")
# Chat interface
avatar_ai=os.getenv('VEL_ICON')
avatar_human=os.getenv('VEL_USER')
  # Display chat 
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI",avatar=avatar_ai):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human", avatar=avatar_human):
            st.markdown(message.content)

# Get user query and display it
user_query = st.chat_input("Ecrivez votre message...")

if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    # Display user query
    with st.chat_message("Human", avatar=avatar_human):
        st.markdown(user_query)
    # Get AI response   
    with st.chat_message("AI",avatar=avatar_ai):
        with st.spinner("Thinking..."):
          ai_response = st.write_stream(get_response(user_query, st.session_state.db, st.session_state.chat_history))
        
    st.session_state.chat_history.append(AIMessage(ai_response))
