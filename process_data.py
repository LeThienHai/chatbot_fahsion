from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from embeddings.sentenceTransformer import SentenceTransformerEmbedding, EmbeddingConfig
import json
import pandas as pd

# Load the environment variables from the .env file
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
DB_COLLECTION = os.getenv('DB_COLLECTION')
LLM_KEY = os.getenv('GEMINI_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') or 'keepitreal/vietnamese-sbert'

df = pd.read_csv('products_2.csv')

def combine_info(row):
    return f"Thương hiệu {row['brand']} với sản phẩm {row['product_name']} có mô tả sản phẩm là {row['description']}, màu sắc là {row['color']} với các kích cỡ {row['size']} được thiết kế bởi vật liệu {row['material']}"

def get_embedding(text):
    embedding_model = SentenceTransformerEmbedding(EmbeddingConfig(name=EMBEDDING_MODEL))
    if not text.strip():
        return []

    embedding = embedding_model.encode(text)
    return embedding.tolist()

df['combined_info'] = df.apply(combine_info, axis=1)
df['embedding'] = df['combined_info'].apply(get_embedding)

# Connect to the MongoDB server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client[DB_NAME]
colection = db[DB_COLLECTION]

data_to_insert = json.loads(df.to_json(orient='records'))

# Insert the data into the collection
colection.insert_many(data_to_insert)
print('Data inserted successfully')