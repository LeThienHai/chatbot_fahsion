from rag.core import RAG
from dotenv import load_dotenv
import os
import pymongo

# Load the environment variables from the .env file
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
DB_COLLECTION = os.getenv('DB_COLLECTION')
LLM_KEY = os.getenv('GEMINI_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') or 'keepitreal/vietnamese-sbert'


def test_rag(query):
    rag = RAG(
        mongodbUri=MONGODB_URI,
        dbName=DB_NAME,
        dbCollection=DB_COLLECTION,
        llm=LLM_KEY,
        embeddingName=EMBEDDING_MODEL
    )

    results = rag.vector_search(query)
    return results


if __name__ == '__main__':
    query = "Sản phẩm Carlie Blouse còn màu trắng không?"
    results = test_rag(query)
    for result in results:
        print(result)
        print('-----------------------------------------------------------')
