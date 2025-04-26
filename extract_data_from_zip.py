import zipfile

# Step 1: Unzip Arabic_Text_Extractor.zip directly into the current directory
with zipfile.ZipFile('Data_until_now.zip', 'r') as zip_ref:
    zip_ref.extractall()

print("Unzipped successfully into the current directory!")

# Step 1: Unzip Arabic_Text_Extractor.zip directly into the current directory
with zipfile.ZipFile('RAA_CUSTOM_DATASET.zip', 'r') as zip_ref:
    zip_ref.extractall()

print("Unzipped successfully into the current directory!")