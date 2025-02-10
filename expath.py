import os
import zipfile

# Step 1: Create directories
os.makedirs('data/train/images', exist_ok=True)
os.makedirs('data/test/images', exist_ok=True)

# Step 2: Unzip the file archive.zip
archive_zip_path = "data/archive.zip"
extract_to_path = "data/"

with zipfile.ZipFile(archive_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_path)

# Step 3: Run the script to extract MNIST images
os.system('python utils/extract_mnist_images.py')


