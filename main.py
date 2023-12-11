
import os
import openai

from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import NLTKTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import PyMuPDFLoader

from pymilvus import Collection, FieldSchema, CollectionSchema, DataType, connections,db


def list_files(initdir: str, file_extensions: list):
    '''
    Returns a list of file under initdir and all its subdirectories
    that have file extension contained in file_extensions.
    ''' 
    file_list = []
    file_count = {key: 0 for key in file_extensions}  # for reporting only
    
    # Traverse through directories to find files with specified extensions
    for root, _, files in os.walk(initdir):
        for file in files:
            ext = file.split('.')[-1].lower()
            if ext in file_extensions:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
                # increment type of file
                file_count[ext] += 1
    
    total = len(file_list)
    print(f'There are {total} files under dir {initdir}.')
    for k, n in file_count.items():
        print(f'   {n} : ".{k}" files')
    return file_list


def convert_and_split(text_splitter, file_path: str) -> list:
    '''
    It converts the file to a textual representation, adds metadata, and
    calls the text_splitter to split long sequences.
    It returns a list of Documents or None is there is any error in the 
    file conversion.
    '''
    text_splitter = NLTKTextSplitter(chunk_size=1000)
    texts = None
    try:
        if file_path.endswith('.pdf'):
            loader = PyMuPDFLoader(file_path)
            pages = loader.load()
            texts = text_splitter.split_documents(pages)

        elif file_path.endswith('.docx') or file_path.endswith('.doc'):
            loader = UnstructuredWordDocumentLoader(file_path)
            docs = loader.load()
            texts = text_splitter.split_documents(docs)
        
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
            docs = loader.load()
            texts = text_splitter.split_documents(docs)

        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            loader = UnstructuredExcelLoader(file_path)
            docs = loader.load()
            texts = text_splitter.split_documents(docs)

        elif file_path.endswith('.csv'):
            loader = CSVLoader(file_path)
            docs = loader.load()
            texts = text_splitter.split_documents(docs)
        
        elif file_path.endswith('.pptx') or file_path.endswith('.ppt'):
            loader = UnstructuredPowerPointLoader(file_path)
            docs = loader.load()
            texts = text_splitter.split_documents(docs)

        else:
            print(f"Error: invalid file type: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return texts

def index_files_milvus(filelst: list, collection_name: str):
    '''
    Given a list of files and a collection name, visit all files, convert them
    to text and metadata, split them into chunks and store their embeddings
    and metadata into Milvus for future semantic search.
    '''
    # define the text_splitter and chunk size
    text_splitter = NLTKTextSplitter(chunk_size=1000)
    
    # define the language model to be used for generating the vector embeddings
    # For security reasons, it is better not to pass the API key directly in
    # the code, use an environment variable.
    # embedding = OpenAIEmbeddings(
    #     model="text-embedding-ada-002",
    #     openai_api_key='insert-your-OpenAI-api-key-here'
    #     )

    # create a schema and a collection using it
    # create_collection_schema(collection_name)

    # bookeeping variables
    error_files = []    # list of files that failed
    cnt = 0             # number of files successfully stored

    # Process each file by calling the appropriate file loader, depending on the file type
    for file_path in filelst:
        cnt += 1
        print(f'=> processing file {cnt} / {len(filelst)}: {file_path}')

        # convert the file into a list of Documents to be stored
        texts = convert_and_split(text_splitter, file_path)

        if not texts:
            error_files.append(file_path)   # keep track of files that failed
            cnt -= 1                        # count only successful conversions
            continue

        # now generate embeddings and store texts and vectors into vector database
        # vector_db = add_docs_to_milvus(texts, embedding, collection_name, file_path)

        # if not vector_db:
        #     error_files.append(file_path)   # keep track of files that failed
        #     cnt -= 1                        # count only successful conversions
        #     continue
        # pass   # end of for loop

    # print summary
    print(f'[index_files] Generated embeddings for {cnt} / {len(filelst)} under dir {initdir}')
    if len(error_files) > 0:
        print(f'              Files with problems:')
        for f in error_files:
            print(f'                 {f}')
    else:
        print(f'              All files successfully processed')
    
    pass  # end of function


if __name__ == "__main__":

    file_extensions = ['pdf', 'doc', 'docx', 'xlsx', 'xls', 'ppt', 'pptx', 'txt', 'csv']
    initdir = os.getcwd()
    dir = os.path.join(initdir, 'Files')

    # define a collection name (it can be any name)
    collection_name='testfiles_repo'

    # visit directory structure and create list of files with given extensions
    filelst = list_files(dir, file_extensions)
   
     
    # visit all files, convert them to text and index them into Milvus
    # index_files_milvus(filelst, collection_name)
    pass





