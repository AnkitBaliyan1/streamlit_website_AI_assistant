from langchain.text_splitter import RecursiveCharacterTextSplitter
#The below import has been replaced by the later one
#from langchain.vectorstores import Pinecone
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
import asyncio
from langchain.document_loaders.sitemap import SitemapLoader
from langchain_openai import OpenAIEmbeddings


import requests
from bs4 import BeautifulSoup

# Function to extract the URL of the sitemap from robots.txt file
def get_sitemap_url(url):
    robots_url = url + "/robots.txt"
    try:
        response = requests.get(robots_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (status code >= 400)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line.startswith("Sitemap:"):
                    return line.split(" ")[1].strip()
            st.warning("No sitemap found in robots.txt")
        else:
            st.warning("Failed to fetch robots.txt")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching robots.txt: {e}")
    return None

# Function to fetch and return the sitemap XML content
def get_sitemap_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            return response.text
        else:
            st.warning("Failed to fetch sitemap XML")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sitemap XML: {e}")
    return None

# Function to fetch data from website
def get_website_data(sitemap_url):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loader = SitemapLoader(sitemap_url)
        docs = loader.load()
        return docs
    except Exception as e:
        st.error(f"Error fetching website data: {e}")
        return None

# Function to split data into smaller chunks
def split_data(docs):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
        docs_chunks = text_splitter.split_documents(docs)
        return docs_chunks
    except Exception as e:
        st.error(f"Error splitting data: {e}")
        return None

# Function to create embeddings instance
def create_embeddings(api_key):
    try:
        embeddings = OpenAIEmbeddings()
        return embeddings
    except Exception as e:
        st.error(f"Error creating embeddings instance: {e}")
        return None

# Function to push data to Pinecone
def push_to_pinecone(pinecone_apikey, pinecone_environment, pinecone_index_name, embeddings, docs):
    try:
        PineconeClient(api_key=pinecone_apikey, environment=pinecone_environment)
        pc = PineconeClient(api_key=pinecone_apikey)
        index = pc.Index(pinecone_index_name)
        index.delete(delete_all=True, namespace='abc')
        st.success("All vectors deleted.")
        index_name = pinecone_index_name
        index = Pinecone.from_documents(docs, embeddings, index_name=index_name, namespace='abc')
        return index
    except Exception as e:
        st.error(f"Error pushing data to Pinecone: {e}")
        return None

# Function to pull index data from Pinecone
def pull_from_pinecone(pinecone_apikey, pinecone_environment, pinecone_index_name, embeddings):
    try:
        PineconeClient(api_key=pinecone_apikey, environment=pinecone_environment)
        index_name = pinecone_index_name
        index = Pinecone.from_existing_index(index_name, embeddings, namespace='abc')
        return index
    except Exception as e:
        st.error(f"Error pulling data from Pinecone: {e}")
        return None

# Function to fetch the top relevant documents from Pinecone Index
def get_similar_docs(index, query, k=2):
    try:
        similar_docs = index.similarity_search(query, k=k)
        return similar_docs
    except Exception as e:
        st.error(f"Error getting similar documents: {e}")
        return None
