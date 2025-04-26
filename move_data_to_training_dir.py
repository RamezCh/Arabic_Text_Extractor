import os
import shutil

# Define source and destination folders
source_folder = 'Data_until_now'
destination_folder = 'tesstrain/data/Arabic_Text_Extractor-ground-truth'

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Move all contents of Tcor to the destination folder
for item in os.listdir(source_folder):
    source_item = os.path.join(source_folder, item)
    destination_item = os.path.join(destination_folder, item)
    shutil.move(source_item, destination_item)
    print(f"Moved {source_item} to {destination_item}")

print("All contents moved successfully!")

# cd tesstrain
# make generate-gt-from-folder-name INPUT_DIR=../RAA_CUSTOM_DATASET/Arabic_Letters OUTPUT_DIR=./data/Arabic_Text_Extractor
# make generate-gt-from-folder-name INPUT_DIR=../RAA_CUSTOM_DATASET/Arabic_Sentences OUTPUT_DIR=./data/Arabic_Text_Extractor

# training now
# make training \
#    TESSDATA=../tessdata \
#    MODEL_NAME=Arabic_Text_Extractor \
#    START_MODEL=ara \
#    MAX_ITERATIONS=8000 \
#    EPOCHS=10 \
#    PSM=7 \
#    LEARNING_RATE=0.0001 \
#    LANG_TYPE=RTL \
#    -l ara

# make training TESSDATA=../tessdata MODEL_NAME=Arabic_Text_Extractor START_MODEL=ara MAX_ITERATIONS=18000 EPOCHS=10 PSM=7 LEARNING_RATE=0.0001 LANG_TYPE=RTL -l ara