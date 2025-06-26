import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the parent directory to the path to import backend modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from backend.database.config import settings
from backend.database.models import Product
from backend.database.init_db import Base
from download_dataset import download_dataset

# Load environment variables from the parent directory
load_dotenv(os.path.join(parent_dir, '.env'))

def insert_data_to_postgres():
    """
    Download dataset and insert data into PostgreSQL database.
    """
    
    print("Starting data insertion process...")
    
    # Step 1: Download the dataset to data folder
    print("Step 1: Downloading dataset...")
    dataset_path, csv_filename = download_dataset()
    
    if not dataset_path or not csv_filename:
        print("Failed to download dataset. Exiting...")
        return
    
    # Step 2: Read the CSV file from data folder
    csv_file_path = os.path.join(dataset_path, csv_filename)
    print(f"Step 2: Reading CSV file: {csv_file_path}")
    
    try:
        data = pd.read_csv(csv_file_path)
        print(f"Successfully loaded {len(data)} rows from CSV")
        print("Columns:", data.columns.tolist())
        print("First few rows:")
        print(data.head())
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Step 3: Connect to PostgreSQL
    print("Step 3: Connecting to PostgreSQL...")
    
    try:
        # Create engine using the database URL from settings
        engine = create_engine(settings.database_url)
        
        # Create tables if they don't exist
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("Successfully connected to PostgreSQL database")
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    
    # Step 4: Insert data
    print("Step 4: Inserting data...")
    
    try:
        inserted_count = 0
        skipped_count = 0
        
        for index, row in data.iterrows():
            try:
                # Check if product already exists
                existing_product = db.query(Product).filter(
                    Product.ProductID == str(row.get('ProductID', ''))
                ).first()
                
                if existing_product:
                    print(f"Product {row.get('ProductID', '')} already exists, skipping...")
                    skipped_count += 1
                    continue
                
                # Create new product
                product = Product(
                    ProductID=str(row.get('ProductID', '')),
                    ProductName=str(row.get('ProductName', '')),
                    ProductBrand=str(row.get('ProductBrand', '')),
                    Gender=str(row.get('Gender', '')),
                    Price=float(row.get('Price', 0)) if pd.notna(row.get('Price')) else 0.0,
                    Description=str(row.get('Description', '')),
                    PrimaryColor=str(row.get('PrimaryColor', ''))
                )
                
                db.add(product)
                inserted_count += 1
                
                # Commit every 100 records for better performance
                if inserted_count % 100 == 0:
                    db.commit()
                    print(f"Inserted {inserted_count} records...")
                    
            except Exception as e:
                print(f"Error inserting row {index}: {e}")
                db.rollback()
                continue
        
        # Final commit
        db.commit()
        
        print(f"Data insertion completed!")
        print(f"Total records inserted: {inserted_count}")
        print(f"Total records skipped: {skipped_count}")
        print(f"Total records processed: {len(data)}")
        
    except Exception as e:
        print(f"Error during data insertion: {e}")
        db.rollback()
    
    finally:
        # Step 5: Close database connection
        print("Step 5: Closing database connection...")
        db.close()
        print("Database connection closed successfully")

def main():
    """Main function to run the data insertion process."""
    try:
        insert_data_to_postgres()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
