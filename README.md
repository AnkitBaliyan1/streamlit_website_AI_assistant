# AI Website Assistant

This Streamlit application serves as an AI assistant for websites, aiding users in finding relevant information efficiently. The assistant utilizes various APIs and services to fetch, process, and present data from a given website. Below are the key functionalities of this application:

## Features:

### 1. Data Loading:
- **Sitemap Extraction**: The application extracts the sitemap URL from the provided website's `robots.txt` file and fetches the corresponding sitemap XML content.

### 2. Data Processing:
- **Data Chunking**: After fetching the website data, it is split into smaller, manageable chunks for efficient processing.

### 3. Embeddings:
- **Embeddings Creation**: Utilizes OpenAI embeddings to create vector representations of text data, facilitating semantic similarity calculations.

### 4. Pinecone Integration:
- **Data Storage and Retrieval**: Utilizes Pinecone, a vector database service, to store and retrieve vector representations of website data efficiently.

### 5. User Interaction:
- **User Input Handling**: Accepts user queries or prompts via text input for information retrieval.
- **Search Results Display**: Displays relevant search results based on the user's query, fetched from the Pinecone index.

## Usage:

1. **API Key Input**: Users are required to input their API keys for Hugging Face, Pinecone, and OpenAI. These keys are necessary for accessing the respective services.

2. **Website URL Input**: Users can input the URL of the website they want to analyze.

3. **Data Loading**: Upon clicking the "Load data to Pinecone" button, the application fetches data from the provided website, processes it, and loads it into the Pinecone index for future retrieval.

4. **User Interaction**: Users can then input their queries or prompts in the provided text box and click the "Search" button to retrieve relevant information.

5. **Search Results Display**: The application displays the top relevant documents along with their information and links from the website.

## Technologies Used:

- **Streamlit**: The user interface is built using Streamlit, a popular Python library for creating interactive web applications.
- **Python**: The backend logic and data processing are implemented in Python.
- **Pinecone**: Utilized for efficient storage and retrieval of vector representations of website data.
- **OpenAI**: Used for generating embeddings (vector representations) of text data.
- **Hugging Face**: Not specified how it's used in the application, but the provision for its API key suggests potential integration for NLP tasks.

This AI Website Assistant streamlines the process of extracting, processing, and retrieving information from websites, offering users an intuitive interface for efficient data interaction and retrieval.
