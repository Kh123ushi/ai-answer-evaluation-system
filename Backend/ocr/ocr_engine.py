# ocr/ocr_engine.py

import easyocr
import cv2
import numpy as np

# Load once when server starts
reader = easyocr.Reader(['en'], gpu=False)


# ===============================
# Image Preprocessing
# ===============================
def preprocess_image(image_path):
    try:
        img = cv2.imread(image_path)

        if img is None:
            return image_path

        # Resize for better OCR
        img = cv2.resize(
            img,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise removal
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # Thresholding
        thresh = cv2.threshold(
            blur,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return thresh

    except Exception as e:
        print("Preprocessing Error:", e)
        return image_path


# ===============================
# OCR Function
# ===============================
def extract_text(image_path):
    try:
        processed_img = preprocess_image(image_path)

        result = reader.readtext(
            processed_img,
            paragraph=True,
            detail=0
        )

        text = " ".join(result)

        return text.strip()

    except Exception as e:
        print("OCR Error:", e)
        return ""