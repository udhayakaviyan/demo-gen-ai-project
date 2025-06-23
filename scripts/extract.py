import pytesseract
from PIL import Image
import cv2
import os
from pptx import Presentation

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    return pytesseract.image_to_string(image)

def extract_text_from_pptx(pptx_path):
    prs = Presentation(pptx_path)
    content = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                content.append(shape.text)
            elif shape.shape_type == 19:  # Table
                for row in shape.table.rows:
                    row_text = [cell.text.strip() for cell in row.cells]
                    content.append("\t".join(row_text))
    return "\n".join(content)

def extract_from_folder(image_folder, pptx_folder):
    docs = []
    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(image_folder, filename)
            text = extract_text_from_image(path)
          #  print("text",text)
            docs.append({"filename": filename, "content": text})
    for filename in os.listdir(pptx_folder):
        if filename.lower().endswith(".pptx"):
            path = os.path.join(pptx_folder, filename)
            text = extract_text_from_pptx(path)
            docs.append({"filename": filename, "content": text})
    
    return docs
