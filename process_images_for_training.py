import os
from PIL import Image, ImageOps


def preprocess_images(input_folder, output_folder, border_size=50):
    """
    Process all images in input_folder:
    1. Convert to grayscale
    2. Add white border
    3. Save as PNG in output_folder with 300 DPI

    Args:
        input_folder (str): Path to folder containing input images
        output_folder (str): Path to save processed images
        border_size (int): Size of white border to add (default: 50 pixels)
    """

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get all files in input folder
    for filename in os.listdir(input_folder):
        try:
            # Build full file paths
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"preprocessed_{os.path.splitext(filename)[0]}.png")

            # Skip if not a file
            if not os.path.isfile(input_path):
                continue

            # Open the image
            with Image.open(input_path) as img:
                # Convert to grayscale
                img_processed = img.convert('L')

                # Add white border
                img_processed = ImageOps.expand(img_processed, border=border_size, fill='white')

                # Save as PNG with 300 DPI
                img_processed.save(output_path, format="PNG", dpi=(300, 300))

            print(f"Processed: {filename} -> saved as {output_path}")

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")


# Example usage:
input_folder = "./tesstrain/data/Arabic_Text_Extractor-ground-truth"
output_folder = "./tesstrain/data/Arabic_Text_Extractor-ground-truth"
preprocess_images(input_folder, output_folder)