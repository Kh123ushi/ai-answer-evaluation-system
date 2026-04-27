import cv2
import pytesseract
import easyocr
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

reader = easyocr.Reader(['en'], gpu=False)


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    # Resize bigger
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Sharpen
    kernel = np.array([[0,-1,0],
                       [-1,5,-1],
                       [0,-1,0]])
    sharp = cv2.filter2D(gray, -1, kernel)

    # Threshold
    thresh = cv2.threshold(
        sharp, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return thresh


def extract_easyocr(image_path):
    result = reader.readtext(image_path, paragraph=True)

    text = " ".join([item[1] for item in result])

    return text.strip()


def extract_tesseract(processed_img):
    pil = Image.fromarray(processed_img)

    text = pytesseract.image_to_string(
        pil,
        config='--oem 3 --psm 6'
    )

    return text.strip()


def extract_text(image_path):
    try:
        processed = preprocess_image(image_path)

        # PRIORITY handwriting OCR
        easy_text = extract_easyocr(image_path)

        # fallback
        tess_text = extract_tesseract(processed)

        # choose smarter
        if len(easy_text.split()) >= 3:
            print("Using EasyOCR")
            return easy_text

        print("Using Tesseract")
        return tess_text

    except Exception as e:
        print("OCR Error:", e)
        return ""