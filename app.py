import streamlit as st
from utils import *
#import constants

# Creating Session State Variable
if 'HuggingFace_API_Key' not in st.session_state:
    st.session_state['HuggingFace_API_Key'] =''
if 'Pinecone_API_Key' not in st.session_state:
    st.session_state['Pinecone_API_Key'] =''

PINECONE_ENVIRONMENT="gcp-starter"
PINECONE_INDEX="chatbotdb"

#
st.title('🤖 AI Assistance For Website') 

#********SIDE BAR Funtionality started*******

# Sidebar to capture the API keys
st.sidebar.title("😎🗝️")
st.session_state['HuggingFace_API_Key']= st.sidebar.text_input("What's your HuggingFace API key?",type="password")
st.session_state['Pinecone_API_Key']= st.sidebar.text_input("What's your Pinecone API key?",type="password")
st.session_state['OPENAI_API_KEY']= st.sidebar.text_input("What's your OPENAI API key?",type="password")
website = st.sidebar.text_input("Enter the website")

#Recent changes by langchain team, expects ""PINECONE_API_KEY" environment variable for Pinecone usage! So we are creating it here
import os
os.environ["PINECONE_API_KEY"] = st.session_state['Pinecone_API_Key']
os.environ["OPENAI_API_KEY"]=st.session_state['OPENAI_API_KEY']


load_button = st.sidebar.button("Load data to Pinecone", key="load_button")

#If the bove button is clicked, pushing the data to Pinecone...
if load_button:
    #Proceed only if API keys are provided
    if st.session_state['HuggingFace_API_Key'] !="" and st.session_state['Pinecone_API_Key']!="" :

        #Fetch data from site
        website_xml = main_xml_url(website)
        if website_xml:
            with st.spinner("loading website data.."):
                site_data = get_website_data(website_xml)
                if site_data:
                    st.sidebar.success("Sitemap content fetched successfully from the given website.")
            #st.write("Data pull done...")

            #Split data into chunks
            chunks_data=split_data(site_data)
            #st.write("Spliting data done...")

            #Creating embeddings instance
            embeddings=create_embeddings(api_key=os.environ["OPENAI_API_KEY"])
            #st.write("Embeddings instance creation done...")

            #Push data to Pinecone
            
            push_to_pinecone(st.session_state['Pinecone_API_Key'],PINECONE_ENVIRONMENT,PINECONE_INDEX,embeddings,chunks_data)
            #st.write("Pushing data to Pinecone done...")

            st.sidebar.success("Data pushed to Pinecone successfully! Ready to take your question")
        else:
            st.write("No sitemap found for the given website.")
            
    else:
        st.sidebar.error("Ooopssss!!! Please provide API keys.....")

#********SIDE BAR Funtionality ended*******

#Captures User Inputs
prompt = st.text_input('How can I help you my friend ❓',key="prompt")  # The box for the text prompt
document_count = st.slider('No.Of links to return 🔗 - (0 LOW || 5 HIGH)', 0, 5, 2,step=1)

submit = st.button("Search") 


if submit:
    #Proceed only if API keys are provided
    if st.session_state['HuggingFace_API_Key'] !="" and st.session_state['Pinecone_API_Key']!="" and st.session_state['Pinecone_API_Key']!="":

        #Creating embeddings instance
        embeddings=create_embeddings(api_key=os.environ["OPENAI_API_KEY"])
        #st.write("Embeddings instance creation done...")

        #Pull index data from Pinecone
        index=pull_from_pinecone(st.session_state['Pinecone_API_Key'],PINECONE_ENVIRONMENT,PINECONE_INDEX,embeddings)
        #st.write("Pinecone index retrieval done...")

        if prompt:
            #Fetch relavant documents from Pinecone index
            relavant_docs=get_similar_docs(index,prompt,document_count)
            #st.write(relavant_docs)

            #Displaying search results
            st.success("Please find the search results :")
            #Displaying search results
            st.write("search results list....")
            for document in relavant_docs:
                
                st.write("👉**Result : "+ str(relavant_docs.index(document)+1)+"**")
                st.write("**Info**: "+document.page_content)
                st.write("**Link**: "+ document.metadata['source'])

        else:
            st.success("I'm ready, you can ask me anything.")

        
      

    else:
        st.sidebar.error("Ooopssss!!! Please provide API keys.....")


   
