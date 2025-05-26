import yaml
import os
import logging

def file_exists(file_path):
    is_exist = os.path.exists(file_path)
    if is_exist:
        logging.info(f"File exists at {file_path}")
        return True
    else:
        logging.warning(f"File does not exist at {file_path}")
        return False

def read_yaml(path_to_yaml: str) -> dict:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        logging.info(f"YAML file loaded: {path_to_yaml}")
        return content
    except Exception as e:
        logging.error(f"Error reading YAML: {e}")
        return {}

def create_dirs(dirs: list):
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        logging.info(f"Directory created: {dir}")
