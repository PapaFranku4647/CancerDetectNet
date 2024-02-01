import gdown
import shutil
import os
import zipfile

## Download Normal Images
normal_url = "https://drive.google.com/uc?id=16uNjw6Ku4EiDUUbED-dL7E4N0PAX_UjH"
normal_file = "Normal_Pics.zip"
normal_path = "../Augmented_Images"

os.makedirs(normal_path, exist_ok=True)

moved_zip_path = os.path.join(normal_path, normal_file)

if not os.path.exists(moved_zip_path):
    gdown.download(normal_url, normal_file, quiet=False)
    shutil.move(normal_file, moved_zip_path)
else:
    print(f"The file {normal_file} is already downloaded in {normal_path}.")

if os.path.exists(moved_zip_path):
    with zipfile.ZipFile(moved_zip_path, 'r') as zip_ref:
        zip_ref.extractall(normal_path)
    print(f"Extracted {normal_file} in {normal_path}.")
else:
    print(f"No need to unzip; {normal_file} does not exist at {moved_zip_path}.")


## Download Malignant Images
malignant_url = "https://drive.google.com/uc?id=1AzRHfp-4ZE5funlESJi9DOis4mwfpjZm"
malignant_file = "Malignant_Pics.zip"
malignant_path = "../Augmented_Images"

os.makedirs(malignant_path, exist_ok=True)

moved_zip_path = os.path.join(malignant_path, malignant_file)

if not os.path.exists(moved_zip_path):
    gdown.download(malignant_url, malignant_file, quiet=False)
    shutil.move(malignant_file, moved_zip_path)
else:
    print(f"The file {malignant_file} is already downloaded in {malignant_path}.")

if os.path.exists(moved_zip_path):
    with zipfile.ZipFile(moved_zip_path, 'r') as zip_ref:
        zip_ref.extractall(malignant_path)
    print(f"Extracted {malignant_file} in {malignant_path}.")
else:
    print(f"No need to unzip; {malignant_file} does not exist at {moved_zip_path}.")

## Download Benign Images
benign_url = "https://drive.google.com/uc?id=1Jnimj1BQLmGmuFvGcc8ffVpiGV1ZIy10"
benign_file = "Benign_Pics.zip"
benign_path = "../Augmented_Images"

os.makedirs(benign_path, exist_ok=True)

moved_zip_path = os.path.join(benign_path, benign_file)

if not os.path.exists(moved_zip_path):
    gdown.download(benign_url, benign_file, quiet=False)
    shutil.move(benign_file, moved_zip_path)
else:
    print(f"The file {benign_file} is already downloaded in {benign_path}.")

if os.path.exists(moved_zip_path):
    with zipfile.ZipFile(moved_zip_path, 'r') as zip_ref:
        zip_ref.extractall(benign_path)
    print(f"Extracted {benign_file} in {benign_path}.")
else:
    print(f"No need to unzip; {benign_file} does not exist at {moved_zip_path}.")