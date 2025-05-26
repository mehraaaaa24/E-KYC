import pandas as pd
from datetime import datetime
import re

def filter_lines(lines):
    start_index = None
    end_index = None

    for i in range(len(lines)):
        line = lines[i]
        if "INCOME TAX DEPARTMENT" in line and start_index is None:
            start_index = i
        if "Signature" in line:
            end_index = i
            break

    filtered_lines = []
    if start_index is not None and end_index is not None:
        for line in lines[start_index:end_index + 1]:
            if len(line.strip()) > 2:
                filtered_lines.append(line.strip())

    return filtered_lines

def create_dataframe(texts):
    lines = filter_lines(texts)
    print("="*20)
    print(lines)
    print("="*20)
    data = []
    try:
        name = lines[2].strip() if len(lines) > 2 else ""
        father_name = lines[3].strip() if len(lines) > 3 else ""
        dob = lines[4].strip() if len(lines) > 4 else ""
        pan = ""
        for i in range(len(lines)):
            if "Permanent Account Number" in lines[i]:
                pan = lines[i+1].strip() if i + 1 < len(lines) else ""
                break
        data.append({"ID": pan, "Name": name, "Father's Name": father_name, "DOB": dob, "ID Type": "PAN"})
    except Exception as e:
        print(f"Error in create_dataframe: {e}")
    return pd.DataFrame(data)


def extract_information(data_string):
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]
    print(words)

    extracted_info = {
        "ID": "",
        "Name": "",
        "Father's Name": "",
        "DOB": "",
        "ID Type": "PAN"
    }

    try:
        if "Name" in words:
            name_index = words.index("Name") + 1
            if name_index < len(words):
                extracted_info["Name"] = words[name_index]

            fathers_name_index = name_index + 2
            if fathers_name_index < len(words):
                extracted_info["Father's Name"] = words[fathers_name_index]

        if "Permanent Account Number Card" in words:
            id_number_index = words.index("Permanent Account Number Card") + 1
            if id_number_index < len(words):
                extracted_info["ID"] = words[id_number_index]

        for i, word in enumerate(words):
            try:
                dob_datetime = datetime.strptime(word, "%d/%m/%Y")
                extracted_info["DOB"] = dob_datetime
                break
            except ValueError:
                continue

    except Exception as e:
        print(f"Error in extract_information: {e}")

    print("Extracted info:", extracted_info)
    return extracted_info


def extract_information1(data_string):
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]

    extracted_info = {
        "ID": "",
        "Name": "",
        "Gender": "",
        "DOB": "",
        "ID Type": "AADHAR"
    }

    try:
        # Extract DOB
        dob_index = None
        for i, word in enumerate(words):
            try:
                dob_datetime = datetime.strptime(word, "%d/%m/%Y")
                extracted_info["DOB"] = dob_datetime
                dob_index = i
                break
            except ValueError:
                continue

        # Heuristic: Name is the word before DOB
        if dob_index is not None and dob_index >= 1:
            extracted_info["Name"] = words[dob_index - 1]

        gender_index = next((i for i, word in enumerate(words) if word.lower() in {"male", "female"}), -1)
        if gender_index != -1:
            extracted_info["Gender"] = words[gender_index]

        pattern1 = re.compile(r'^\d{4} \d{4} \d{4}$')
        pattern2 = re.compile(r'^\d{4}$')

        id_number_index1 = next((i for i, word in enumerate(words) if pattern1.match(word)), -1)
        id_number_index2 = next((i for i, word in enumerate(words) if pattern2.match(word)), -1)

        if id_number_index1 != -1:
            extracted_info["ID"] = words[id_number_index1]
        elif id_number_index2 != -1 and id_number_index2 + 2 < len(words):
            extracted_info["ID"] = words[id_number_index2] + words[id_number_index2 + 1] + words[id_number_index2 + 2]

    except Exception as e:
        print(f"Error in extract_information1: {e}")

    print("Extracted info (Aadhar):", extracted_info)
    return extracted_info
