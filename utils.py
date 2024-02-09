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

def get_sitemap_url(url):
    """
    Function to extract the URL of the sitemap from robots.txt file
    """
    robots_url = url + "/robots.txt"
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            # Parsing robots.txt to find sitemap URL
            for line in response.text.split('\n'):
                if line.startswith("Sitemap:"):
                    return line.split(" ")[1].strip()
            print("No sitemap found in robots.txt")
        else:
            print("Failed to fetch robots.txt")
    except requests.exceptions.RequestException as e:
        print("Error fetching robots.txt:", e)
    return None

def get_sitemap_xml(url):
    """
    Function to fetch and return the sitemap XML content
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch sitemap XML")
    except requests.exceptions.RequestException as e:
        print("Error fetching sitemap XML:", e)
    return None


def main_xml_url(given_url):
    website_url = given_url.strip()
    sitemap_url = get_sitemap_url(website_url)
    if sitemap_url:
        print("Sitemap URL found:", sitemap_url)
        sitemap_xml = get_sitemap_xml(sitemap_url)
        if sitemap_xml:
            # Print or process the sitemap XML content here
            print("Sitemap XML content:\n", sitemap_xml)
            return sitemap_url
    else:
        print("No sitemap found for the given website.")


#Function to fetch data from website
#https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/sitemap
def get_website_data(sitemap_url):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loader = SitemapLoader(
    sitemap_url
    )

    docs = loader.load()

    return docs

#Function to split data into smaller chunks
def split_data(docs):

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    )

    docs_chunks = text_splitter.split_documents(docs)
    return docs_chunks

#Function to create embeddings instance
def create_embeddings(api_key):

    OPENAI_API_KEY = api_key
    embeddings = OpenAIEmbeddings()
    return embeddings

#Function to push data to Pinecone
def push_to_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,docs):

    PineconeClient(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    pc = PineconeClient(
            api_key=pinecone_apikey
        )
    index = pc.Index(pinecone_index_name)
    index.delete(delete_all=True, namespace='abc')
    print("all vector deleted.")

    index_name = pinecone_index_name
    #PineconeStore is an alias name of Pinecone class, please look at the imports section at the top :)
    index =  Pinecone.from_documents(docs, embeddings, index_name=index_name, namespace = 'abc')
    return index

#Function to pull index data from Pinecone
def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):

    PineconeClient(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    index_name = pinecone_index_name
    #PineconeStore is an alias name of Pinecone class, please look at the imports section at the top :)
    index = Pinecone.from_existing_index(index_name, embeddings, namespace='abc')
    return index

#This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
def get_similar_docs(index,query,k=2):

    similar_docs = index.similarity_search(query, k=k)
    return similar_docs


