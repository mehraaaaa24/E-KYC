import cv2
import numpy as np
import os
import logging
from utils import read_yaml, file_exists

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

config_path = "config.yaml"
config = read_yaml(config_path)

artifacts = config['artifacts']
intermediate_dir_path = artifacts['INTERMIDEIATE_DIR']
conour_file_name = artifacts['CONTOUR_FILE']

def read_image(image_path, is_uploaded=False):
    try:
        if is_uploaded:
            image_bytes = image_path.read()
            img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        else:
            img = cv2.imread(image_path)

        if img is None:
            raise ValueError("Image data could not be decoded or found.")

        return img
    except Exception as e:
        logging.error(f"Error reading image: {e}")
        return None

def extract_id_card(img):
    try:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray_img, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = None
        largest_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > largest_area:
                largest_contour = cnt
                largest_area = area

        if largest_contour is None:
            logging.warning("No valid contour found in image.")
            return None, None

        x, y, w, h = cv2.boundingRect(largest_contour)
        logging.info(f"ID card contours found at: {(x, y, w, h)}")

        contour_id = img[y:y+h, x:x+w]
        filename = os.path.join(os.getcwd(), intermediate_dir_path, conour_file_name)

        if file_exists(filename):
            os.remove(filename)

        cv2.imwrite(filename, contour_id)
        return contour_id, filename

    except Exception as e:
        logging.error(f"Error extracting ID card region: {e}")
        return None, None

def save_image(image, filename, path="."):
    try:
        full_path = os.path.join(path, filename)
        if file_exists(full_path):
            os.remove(full_path)

        cv2.imwrite(full_path, image)
        logging.info(f"Image saved at: {full_path}")
        return full_path

    except Exception as e:
        logging.error(f"Error saving image: {e}")
        return None
