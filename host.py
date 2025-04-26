from PIL import Image, ImageOps
import pytesseract
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import os
import tempfile
import cv2
import numpy as np
import gradio as gr

def get_psm_mode(image):
    """
    Automatically determines the best PSM mode based on image analysis.
    """
    # Convert to OpenCV format
    image_cv = np.array(image)
    gray = image_cv

    # Apply threshold to segment text
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours (text blocks)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Heuristic for selecting PSM mode
    num_contours = len(contours)

    if num_contours < 5:
        return 6  # Paragraph mode
    elif num_contours < 15:
        return 7  # Single-line mode
    elif num_contours > 50:
        return 11  # Sparse text mode
    else:
        return 3  # Default auto mode

def testModel(imgURL, modelName, tdLocation):
    """
    This function loads the traineddata from Tesseract training and utilizes it to extract text from images.
    It shows the pre-processed image.

    # Parameters:
    imgURL: the directory or the URL of the image
    modelName: the name of the model or simply what is written before .traineddata
    tdLocation: the path to the traineddata file

    # Example usage:
    testModel("https://example.com/path/to/image.jpg", "ara", "/content/tessdata")
    testModel(r"/content/khatt/validate_data/AHTD3A0001_Para1_3.jpg", "ara", "/content/tessdata")
    """
    # Load image from URL or local path
    if imgURL.startswith(('http://', 'https://')):
        response = requests.get(imgURL)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(imgURL)

    # Pre-process the image
    img_processed = img.copy()
    # Turn image into greyscale
    img_processed = img_processed.convert('L')
    # Add a 10px white border
    img_processed = ImageOps.expand(img_processed, border=50, fill='white')
    # Save the pre-processed image as a PNG file
    png_path = "preprocessed_image.png"
    img_processed.save(png_path, format="PNG", dpi=(300, 300))

    # Display the pre-processed image
    plt.figure(figsize=(6, 6))
    plt.imshow(img_processed, cmap="gray")
    plt.title("Pre-processed Image (PNG)")
    plt.axis('off')
    plt.show()

    # Get dynamic PSM mode
    psm_mode = get_psm_mode(img_processed)

    # Perform OCR on the pre-processed PNG image
    text = pytesseract.image_to_string(
        png_path,
        lang=modelName,
        config = f'--tessdata-dir {tdLocation} --oem 1 --psm {psm_mode}'
    )
    print("Extracted Text:\n", text)

    # Clean up the temporary PNG file
    os.remove(png_path)

    return text

def gradio_interface(img_url, img_file):
    try:
        if img_file:
            input_img = img_file
            display_img = img_file
        elif img_url:
            input_img = img_url
            display_img = img_url
        else:
            return "No image provided", None, None, None

        # Extract text from image
        extracted_text = testModel(input_img, "Arabic_Text_Extractor", "tessdata")

        # Create temporary file with actual extracted content
        temp_dir = tempfile.mkdtemp()
        text_file_path = os.path.join(temp_dir, "extracted_text.txt")
        with open(text_file_path, "w", encoding="utf-8") as file:
            file.write(extracted_text)  # Write the actual extracted text

        # Create HTML display with the actual extracted text
        extracted_text_html = f"""
        <div style='
            font-weight: bold;
            white-space: pre-wrap;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 5px;
            background: #f9f9f9;
            margin-bottom: 15px;
        '>
            {extracted_text}
        </div>
        """

        return display_img, extracted_text_html, text_file_path, gr.update(visible=True)

    except Exception as e:
        error_msg = f"<div style='color: red; font-weight: bold;'>Error: {str(e)}</div>"
        return None, error_msg, None, gr.update(visible=False)

def clear_inputs():
    return "", None, "", None, gr.update(visible=False)

with gr.Blocks(css="""
    .orange-button { background-color: orange !important; color: white !important; }
    .download-btn { background-color: #4CAF50 !important; color: white !important; }
    .text-display { font-family: monospace; }
""") as iface:

    gr.Markdown("# <center>Arabic Text Extractor</center>")

    with gr.Row():
        with gr.Column():
            img_url = gr.Textbox(label="Image URL", placeholder="Enter image URL here...")
            img_file = gr.Image(label="Or Upload Image", type="filepath")
            with gr.Row():
                btn_extract = gr.Button("Extract Text", variant="primary")
                btn_clear = gr.Button("Clear All", variant="secondary")

        with gr.Column():
            image_display = gr.Image(label="Input Image Preview")
            gr.Markdown("### Extracted Text:")
            extracted_text = gr.HTML()
            download_btn = gr.DownloadButton(
                "⬇️ Download Text File",
                visible=False,
                elem_classes="download-btn"
            )

    # Input toggling
    def toggle_inputs(img_url, img_file):
        disable_url = img_file is not None
        disable_file = bool(img_url)
        return gr.update(interactive=not disable_url), gr.update(interactive=not disable_file)

    # Event handlers
    img_url.change(toggle_inputs, inputs=[img_url, img_file], outputs=[img_url, img_file])
    img_file.change(toggle_inputs, inputs=[img_url, img_file], outputs=[img_url, img_file])

    # Extract text
    btn_extract.click(
        gradio_interface,
        inputs=[img_url, img_file],
        outputs=[image_display, extracted_text, download_btn, download_btn]
    )

    # Clear all
    btn_clear.click(
        clear_inputs,
        outputs=[img_url, img_file, image_display, extracted_text, download_btn]
    )

iface.launch(share=True)