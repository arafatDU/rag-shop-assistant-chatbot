import os
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from tqdm.auto import tqdm
from dotenv import load_dotenv
import pandas as pd

# Add the parent directory to the path to import backend modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from backend.database.config import settings
from backend.database.models import Product

load_dotenv()

# Pinecone Configuration
api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=api_key)

index_name = "shop-product-catalog"
existing_indexes = [index.name for index in pc.list_indexes()]

# Check if index already exists
if index_name not in existing_indexes:
    # For this example, we'll assume the index already exists
    # If you need to create it, you'll need ServerlessSpec or PodSpec
    print(f"Index {index_name} not found. Please create it manually in Pinecone dashboard.")
    print("Index should have dimension=768 and metric='dotproduct'")
    exit(1)

# Connect to the index
index = pc.Index(index_name)
time.sleep(1)

# Connect to PostgreSQL using SQLAlchemy
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Google GenAI API
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
embed_model=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def fetch_data():
    """Fetch data from PostgreSQL using SQLAlchemy"""
    try:
        products = db.query(Product).all()
        
        # Convert to DataFrame
        data = []
        for product in products:
            data.append({
                'ProductID': product.ProductID,
                'ProductName': product.ProductName,
                'ProductBrand': product.ProductBrand,
                'Gender': product.Gender,
                'Price': product.Price,
                'Description': product.Description,
                'PrimaryColor': product.PrimaryColor
            })
        
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def sync_with_pinecone(data):
    """Sync data with Pinecone vector store"""
    if data.empty:
        print("No data to sync")
        return
    
    batch_size=100
    total_batches=(len(data)+batch_size -1) // batch_size

    for i in tqdm(range(0,len(data),batch_size),desc="Processing Batches",unit='batch',total=total_batches):
        i_end=min(len(data),i + batch_size)
        batch=data.iloc[i:i_end]

        # unique id
        ids=[str(row['ProductID']) for _,row in batch.iterrows()]

        # combine text field for embedding
        texts=[
            f"{row['Description']} {row['ProductName']} {row['ProductBrand']} {row['Gender']} {row['Price']} {row['PrimaryColor']}"
            for _,row in batch.iterrows()
        ]

        # embed texts
        embeds=embed_model.embed_documents(texts)

        # get metadata
        metadata=[
            {
                'ProductName':row['ProductName'],
                'ProductBrand':row['ProductBrand'],
                'Gender':row['Gender'],
                'Price':row['Price'],
                'PrimaryColor':row['PrimaryColor'],
                'Description':row['Description'],
            }
            for _,row in batch.iterrows()
        ]

        # upsert vectors
        with tqdm(total=len(ids),desc="Upserting Vectors",unit='vector') as upsert_vector:
            index.upsert(vectors=zip(ids,embeds,metadata))
            upsert_vector.update(len(ids))

def main():
    """Main function to sync data with Pinecone"""
    try:
        print("Fetching data from PostgreSQL...")
        data = fetch_data()
        print(f"Found {len(data)} products")
        
        if not data.empty:
            print("Syncing with Pinecone...")
            sync_with_pinecone(data)
            print("Sync completed successfully!")
        else:
            print("No data to sync")
    except Exception as e:
        print(f"Error during sync: {e}")
    finally:
        # Close database connection
        db.close()
        print("Database connection closed")

if __name__=="__main__":
    main()
