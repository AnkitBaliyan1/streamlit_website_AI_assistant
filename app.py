import streamlit as st
from utils import *
#import constants

# Main function
def main():
    st.title('🤖 AI Assistance For Website')


    # Creating Session State Variable
    if 'HuggingFace_API_Key' not in st.session_state:
        st.session_state['HuggingFace_API_Key'] =''
    if 'Pinecone_API_Key' not in st.session_state:
        st.session_state['Pinecone_API_Key'] =''
    
    # Sidebar to capture the API keys
    st.sidebar.title("😎🗝️")
    st.session_state['HuggingFace_API_Key'] = st.sidebar.text_input("What's your HuggingFace API key?", type="password")
    st.session_state['Pinecone_API_Key'] = st.sidebar.text_input("What's your Pinecone API key?", type="password")
    st.session_state['OPENAI_API_KEY'] = st.sidebar.text_input("What's your OPENAI API key?", type="password")
    website = st.sidebar.text_input("Enter the website")

    PINECONE_ENVIRONMENT="gcp-starter"
    PINECONE_INDEX="chatbotdb"
    
    load_button = st.sidebar.button("Load data to Pinecone", key="load_button")
    
    if load_button:
        if st.session_state['HuggingFace_API_Key'] and st.session_state['Pinecone_API_Key'] and st.session_state['OPENAI_API_KEY']:
            website_xml = get_sitemap_url(website)
            if website_xml:
                with st.spinner("Loading website data..."):
                    site_data = get_website_data(website_xml)
                    if site_data:
                        st.sidebar.success("Sitemap content fetched successfully from the given website.")
                chunks_data = split_data(site_data)
                embeddings = create_embeddings(api_key=st.session_state['OPENAI_API_KEY'])
                if embeddings:
                    index = push_to_pinecone(st.session_state['Pinecone_API_Key'], "gcp-starter", "chatbotdb", embeddings, chunks_data)
                    if index:
                        st.sidebar.success("Data pushed to Pinecone successfully! Ready to take your question")
                    else:
                        st.sidebar.error("Failed to push data to Pinecone.")
                else:
                    st.sidebar.error("Failed to create embeddings instance.")
            else:
                st.sidebar.error("No sitemap found for the given website.")
        else:
            st.sidebar.error("Please provide API keys.")

    prompt = st.text_input('How can I help you?', key="prompt")
    document_count = st.slider('Number of links to return:', 0, 5, 2, step=1)
    submit = st.button("Search")

    if submit:
        if st.session_state['HuggingFace_API_Key'] and st.session_state['Pinecone_API_Key'] and st.session_state['OPENAI_API_KEY']:
            embeddings = create_embeddings(api_key=st.session_state['OPENAI_API_KEY'])
            if embeddings:
                index = pull_from_pinecone(st.session_state['Pinecone_API_Key'], "gcp-starter", "chatbotdb", embeddings)
                if index:
                    if prompt:
                        relevant_docs = get_similar_docs(index, prompt, document_count)
                        if relevant_docs:
                            st.success("Please find the search results:")
                            for document in relevant_docs:
                                st.write(f"Result: {relevant_docs.index(document)+1}")
                                st.write(f"Info: {document.page_content}")
                                st.write(f"Link: {document.metadata['source']}")
                        else:
                            st.error("Failed to get search results.")
                    else:
                        st.success("I'm ready, you can ask me anything.")
                else:
                    st.error("Failed to pull data from Pinecone.")
            else:
                st.error("Failed to create embeddings instance.")
        else:
            st.error("Please provide API keys.")
            
if __name__ == "__main__":
    main()
