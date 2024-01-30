import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


import os
import pandas as pd
import shutil

cbis_csv = pd.read_csv("cbis.csv")
inbreast_csv = pd.read_csv("inbreast.csv")
mias_csv = pd.read_csv("mias.csv")


cbis_png_directory = 'CBIS'
inbreast_png_directory = 'INbreast'
mias_png_directory = 'MIAS'


benign_folder_path = 'Benign_Pics'
malignant_folder_path = 'Malignant_Pics'
normal_folder_path = 'Normal_Pics'

os.makedirs(benign_folder_path, exist_ok=True)
os.makedirs(malignant_folder_path, exist_ok=True)
os.makedirs(normal_folder_path, exist_ok=True)

count = 0

for row in cbis_csv.values:
    cbis_image_pathology = row[1] # Get Pathology
    cbis_image_num = row[0].split('/')[2].split('.')[0] # Get Image Num

    for file in os.listdir(cbis_png_directory):
        if file.split('_')[0] == cbis_image_num:
            source_path = os.path.join(cbis_png_directory, file)

            has_match = True

            if cbis_image_pathology == "BENIGN":
                target_path = os.path.join(benign_folder_path, f"{file.split('.')[0]}_cbis.png")
            elif cbis_image_pathology == "MALIGNANT":
                target_path = os.path.join(malignant_folder_path, f"{file.split('.')[0]}_cbis.png")
            elif cbis_image_pathology == "NORMAL":
                target_path = os.path.join(normal_folder_path, f"{file.split('.')[0]}_cbis.png")
            else:
                has_match = False
            
            if has_match: shutil.copy(source_path, target_path)

            count+=1


for row in inbreast_csv.values:
    inbreast_image_pathology = row[1] # Get Pathology
    inbreast_image_num = row[0].split('/')[2].split('.')[0] # Get Image Num

    for file in os.listdir(inbreast_png_directory):
        if file.split('_')[0] == inbreast_image_num:
            source_path = os.path.join(inbreast_png_directory, file)

            has_match = True

            if inbreast_image_pathology == "BENIGN":
                target_path = os.path.join(benign_folder_path, f"{file.split('.')[0]}_inbreast.png")
            elif inbreast_image_pathology == "MALIGNANT":
                target_path = os.path.join(malignant_folder_path, f"{file.split('.')[0]}_inbreast.png")
            elif inbreast_image_pathology == "NORMAL":
                target_path = os.path.join(normal_folder_path, f"{file.split('.')[0]}_inbreast.png")
            else:
                has_match = False
            
            if has_match: shutil.copy(source_path, target_path)

            count+=1

for row in mias_csv.values:
    mias_image_pathology = row[1] # Get Pathology
    mias_image_num = row[0].split('/')[2].split('.')[0] # Get Image Num

    for file in os.listdir(mias_png_directory):
        if file.split('_')[0] == mias_image_num:
            source_path = os.path.join(mias_png_directory, file)

            has_match = True

            if mias_image_pathology == "BENIGN":
                target_path = os.path.join(benign_folder_path, f"{file.split('.')[0]}_mias.png")
            elif mias_image_pathology == "MALIGNANT":
                target_path = os.path.join(malignant_folder_path, f"{file.split('.')[0]}_mias.png")
            elif mias_image_pathology == "NORMAL":
                target_path = os.path.join(normal_folder_path, f"{file.split('.')[0]}_mias.png")
            else:
                has_match = False
            
            if has_match: shutil.copy(source_path, target_path)

            count+=1