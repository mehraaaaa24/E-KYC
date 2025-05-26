from deepface import DeepFace
import cv2
import os
import logging
from utils import file_exists, read_yaml

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

config_path = "config.yaml"
config = read_yaml(config_path)

artifacts = config['artifacts']
cascade_path = artifacts['HAARCASCADE_PATH']
output_path = artifacts['INTERMIDEIATE_DIR']

def detect_and_extract_face(img):
    try:
        logging.info("Starting face extraction process...")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

        max_area = 0
        largest_face = None
        for (x, y, w, h) in faces:
            area = w * h
            if area > max_area:
                max_area = area
                largest_face = (x, y, w, h)

        if largest_face is not None:
            (x, y, w, h) = largest_face
            new_w = int(w * 1.50)
            new_h = int(h * 1.50)
            new_x = max(0, x - int((new_w - w) / 2))
            new_y = max(0, y - int((new_h - h) / 2))

            extracted_face = img[new_y:new_y+new_h, new_x:new_x+new_w]
            filename = os.path.join(os.getcwd(), output_path, "extracted_face.jpg")

            if os.path.exists(filename):
                os.remove(filename)

            cv2.imwrite(filename, extracted_face)
            logging.info(f"Extracted face saved at: {filename}")
            return filename
        else:
            logging.warning("No face detected in the image.")
            return None

    except Exception as e:
        logging.error(f"Exception during face detection: {e}")
        return None

def deepface_face_comparison(image1_path, image2_path):
    logging.info("Verifying faces using DeepFace...")

    if not (file_exists(image1_path) and file_exists(image2_path)):
        logging.warning("One or both image paths are invalid.")
        return False

    try:
        verification = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)
        logging.info(f"DeepFace result: {verification}")

        if verification.get('verified'):
            logging.info("Face verification successful.")
            return True
        else:
            logging.info("Face verification failed.")
            return False

    except Exception as e:
        logging.error(f"Error during DeepFace verification: {e}")
        return False

def get_face_embeddings(image_path):
    logging.info(f"Extracting embeddings from: {image_path}")

    if not file_exists(image_path):
        logging.warning(f"Image path does not exist: {image_path}")
        return None

    try:
        embedding_objs = DeepFace.represent(img_path=image_path, model_name="Facenet")
        embedding = embedding_objs[0].get("embedding", [])

        if embedding:
            logging.info("Successfully retrieved face embeddings.")
            return embedding
        else:
            logging.warning("No embeddings returned.")
            return None

    except Exception as e:
        logging.error(f"Exception while retrieving face embeddings: {e}")
        return None
