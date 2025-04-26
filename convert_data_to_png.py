import os
from PIL import Image

# Step 1: Define the input folder
input_folder = 'Data_until_now'  # Folder containing .jpeg images

# Step 2: Convert .jpeg to .png and delete the original .jpeg files
for filename in os.listdir(input_folder):
    if filename.endswith('.jpeg') or filename.endswith('.jpg'):
        # Open the .jpeg image
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Define the output path with .png extension
        output_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(input_folder, output_filename)

        # Save the image in .png format
        img.save(output_path, format='PNG')
        print(f"Converted {filename} to {output_filename}")

        # Delete the original .jpeg file
        os.remove(img_path)
        print(f"Deleted {filename}")

print("All images converted and original .jpeg files deleted successfully!")

# Step 1: Define the input folder
input_folder = 'RAA_CUSTOM_DATASET'  # Root folder containing images

# Supported image extensions to convert (add more if needed)
supported_extensions = ('.jpeg', '.jpg', '.bmp', '.tiff', '.gif', '.webp')

# Step 2: Recursively convert images to PNG and delete originals
for root, dirs, files in os.walk(input_folder):
    for filename in files:
        # Check if file has an extension we want to convert
        if filename.lower().endswith(supported_extensions):
            # Get full file path
            img_path = os.path.join(root, filename)

            try:
                # Open the image
                img = Image.open(img_path)

                # Define the output path with .png extension
                output_filename = os.path.splitext(filename)[0] + '.png'
                output_path = os.path.join(root, output_filename)

                # Save the image in .png format
                img.save(output_path, format='PNG')
                print(f"Converted {img_path} to {output_path}")

                # Close the image file
                img.close()

                # Delete the original file
                os.remove(img_path)
                print(f"Deleted original {img_path}")

            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")

print("Conversion process completed!")