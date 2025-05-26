import os
import easyocr
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

def extract_text(image_path, confidence_threshold=0.3, languages=['en']):
    logging.info("Text Extraction Started...")
    reader = easyocr.Reader(languages)

    try:
        logging.info("Initializing OCR reader and processing image...")
        result = reader.readtext(image_path)

        filtered_text = "|"  # Delimiter used in downstream processing
        for bbox, text, confidence in result:
            logging.info(f"OCR Output: '{text}' (Confidence: {confidence:.2f})")
            if confidence > confidence_threshold:
                filtered_text += text + "|"

        if not filtered_text.strip("|"):
            logging.warning("No text passed the confidence threshold.")

        logging.info(f"Final Extracted Text: {filtered_text}")
        return filtered_text

    except Exception as e:
        logging.error(f"An error occurred during text extraction: {e}")
        return ""
