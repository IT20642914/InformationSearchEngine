# InformationSearchEngine
A full search system using Solr was developed to find technical information, but it didn't summarize data from various sources. To improve, two flows should be implemented: collecting file information and understanding user questions, and displaying relevant information in a natural language format.


#Frameworks and Tools
OpenAI -OpenAI provides LLMs, although not free, which are relatively cheap and easy to use for our purposes.
For the generation of the embeddings I will use model text-embedding-ada-002 which has a cost of $0.0001 for 1K tokens. For the user query LLM I will use GPT3.5 Turbo which has a cost between $0.0015 and $0.002 for 1K tokens. According to OpenAI, as a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text.

*#Langchain
LangChain is a software framework with higher-level classes and methods for accessing language models and vector databases, enabling uniform interfaces and enabling the development of new applications, including chains for specific use-cases like chatbots.

#Milvus (Vector DB)
Milvus is a vector database, where the data stored are primarily vector embeddings and data retrieval is done through vector similarity search algorithms, such as ANN (approximate nearest neighbors). Milvus is open-source software with an active and helpful community.

