import warnings

# Filter out DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

import cv2
import numpy as np
import pandas as pd
import pydicom
import os

dicom_directory = "INbreast Release 1.0\AllDICOMs"
jpeg_path = "INbreast_Trimmed\jpeg_full"
csv_path = "INbreast_Trimmed\csv"

if not os.path.exists(csv_path):
    os.makedirs(csv_path)


sheet_1 = pd.read_excel("INbreast Release 1.0\INbreast.xls", sheet_name="Sheet1")

mass_sheet_1 = sheet_1[sheet_1['Mass ']=="X"]
mass_sheet_1_filtered = mass_sheet_1[['File Name', 'Bi-Rads']]
# Not considering Maybes (4a, 4b, 4c)
mass_sheet_1_filtered = mass_sheet_1_filtered[mass_sheet_1_filtered['Bi-Rads'].isin([1, 2, 3, 5, 6])]

def label_mass(mass_sheet):
    pathology_mapping = {
        1: 'BENIGN',
        2: 'BENIGN',
        3: 'BENIGN',
        5: 'MALIGNANT',
        6: 'MALIGNANT',
    }

    # Create a new 'Pathology' column based on the 'Bi-Rads' column
    mass_sheet['Pathology'] = mass_sheet['Bi-Rads'].map(pathology_mapping)

def count_masses(mass_sheet):
    malignant_count = len(mass_sheet_1_filtered[mass_sheet_1_filtered['Pathology']=="MALIGNANT"])
    benign_count = len(mass_sheet_1_filtered[mass_sheet_1_filtered['Pathology']=="BENIGN"])
    print("Malignant Count:", malignant_count)
    print("Benign Count:", benign_count)




def mass_row_to_image_path(mass_row):
    jpeg_path = "INbreast_Trimmed\jpeg_full"
    image_num = str(int(mass_row[0]))
    pattern = f"{image_num}*.dcm"
    matching_files = [file for file in os.listdir(dicom_directory) if file.startswith(image_num)]
    if matching_files:
        if(len(matching_files) > 1):
            print("Too Many Matches")
            return None
        else:
            
            dicom_file_path = os.path.join(dicom_directory, matching_files[0])
            dicom_data = pydicom.dcmread(dicom_file_path).pixel_array

            image_array = cv2.normalize(dicom_data, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imwrite(f'{jpeg_path}\{image_num}.jpg', image_array)
            jpeg_path = f'{jpeg_path}\{image_num}.jpg'
            return jpeg_path
    return None



label_mass(mass_sheet_1_filtered)


jpeg_file_paths = []
for row in mass_sheet_1_filtered.values.tolist():
    jpeg_file_path = mass_row_to_image_path(row)
    jpeg_file_paths.append(jpeg_file_path)

mass_sheet_1_filtered["JPEG Path"] = jpeg_file_paths

csv_file_path = os.path.join(csv_path, "original_filtered.csv")
mass_sheet_1_filtered.to_csv(csv_file_path, index=False)