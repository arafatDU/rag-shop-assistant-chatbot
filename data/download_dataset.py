import kagglehub
import os
import shutil

def download_dataset():
    """Download the shop product catalog dataset from Kaggle to the data folder."""
    
    print("Downloading shop product catalog dataset...")
    
    # Get the current directory (data folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Download latest version to default kagglehub location first
    downloaded_path = kagglehub.dataset_download("supratimnag06/shop-product-catalog")
    
    print("Downloaded to kagglehub cache:", downloaded_path)
    
    # Copy files to the data folder
    if os.path.exists(downloaded_path):
        files = os.listdir(downloaded_path)
        print("Downloaded files:", files)
        
        # Look for CSV files and copy them to data folder
        csv_files = [f for f in files if f.endswith('.csv')]
        if csv_files:
            print(f"Found CSV files: {csv_files}")
            
            # Copy the first CSV file to data folder
            source_csv = os.path.join(downloaded_path, csv_files[0])
            dest_csv = os.path.join(current_dir, csv_files[0])
            
            try:
                shutil.copy2(source_csv, dest_csv)
                print(f"Copied {csv_files[0]} to {current_dir}")
                return current_dir, csv_files[0]  # Return data folder path and CSV filename
            except Exception as e:
                print(f"Error copying file: {e}")
                return downloaded_path, csv_files[0]  # Return original path if copy fails
        else:
            print("No CSV files found in the downloaded dataset")
            return downloaded_path, None
    else:
        print("Download path does not exist")
        return None, None

if __name__ == "__main__":
    dataset_path, csv_file = download_dataset()
    if dataset_path and csv_file:
        print(f"Dataset successfully downloaded to: {dataset_path}")
        print(f"CSV file: {csv_file}")
    else:
        print("Failed to download dataset")
