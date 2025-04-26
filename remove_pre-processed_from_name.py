import os


def rename_preprocessed_files(folder_path):
    """
    Removes 'preprocessed_' prefix from all PNG files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing the files to rename
    """
    # Get all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a PNG and starts with 'preprocessed_'
        if filename.lower().endswith('.png') and filename.startswith('preprocessed_'):
            # Create the new filename by removing 'preprocessed_'
            new_filename = filename[len('preprocessed_'):]

            # Full paths for old and new names
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

            # Rename the file
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Error renaming {filename}: {str(e)}")


# Example usage:
folder_path = "./tesstrain/data/Pre-Processed_Arabic_Text_Extractor-ground-truth"
rename_preprocessed_files(folder_path)