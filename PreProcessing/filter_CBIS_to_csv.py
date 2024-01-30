# Filter out pandas depreciation warning
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import packages
import csv
import os
import pandas as pd


dicom_csv = pd.read_csv("CBIS-DDSM/csv/dicom_info.csv")
mass_train = pd.read_csv("CBIS-DDSM/csv/mass_case_description_train_set.csv")
calc_train = pd.read_csv("CBIS-DDSM/csv/calc_case_description_train_set.csv")
mass_test = pd.read_csv("CBIS-DDSM/csv/mass_case_description_test_set.csv")
calc_test = pd.read_csv("CBIS-DDSM/csv/calc_case_description_test_set.csv")

dicom_trimmed = dicom_csv[["image_path", "PatientID", "Laterality", 'SeriesDescription']]


dicom_train_mask = dicom_trimmed['PatientID'].str.startswith(('Calc-Training', 'Mass-Training'))
dicom_test_mask = dicom_trimmed['PatientID'].str.startswith(('Calc-Test', 'Mass-Test'))

series_description_mask = dicom_trimmed['SeriesDescription'] == 'full mammogram images'


dicom_train = dicom_trimmed[dicom_train_mask & series_description_mask]
dicom_train = dicom_train[['PatientID', 'image_path', 'SeriesDescription', 'Laterality']].values.tolist()

dicom_test = dicom_trimmed[dicom_test_mask & series_description_mask]
dicom_test = dicom_test[['PatientID', 'image_path', 'SeriesDescription', 'Laterality']].values.tolist()




def ID_to_patient(dicom_row, count, data_to_save):
    """
    Converts an patient_ID from the dicom dataset into the correct location/patient in the description dataset
    """
    
    patient_id = dicom_row[0]
    image_path = dicom_row[1]
    
    # Extracts features
    parts = patient_id.split('_')
    dataset_type = parts[0] # Mass-Training, Calc-Training, Mass-Test, Calc-Test
    patient_id = ('_').join([parts[1],parts[2]])
    laterality = parts[3]  # Extract the laterality (e.g., RIGHT or LEFT)
    view = parts[4]  # Extract the view (e.g., MLO or CC)
    
    # Checks to make sure features are valid
    if dataset_type not in {"Mass-Training", "Calc-Training", "Mass-Test", "Calc-Test"}:
        print(f"Error: Invalid dataset_type '{dataset_type}'")
    else:
        if dataset_type == 'Mass-Training':
            # print(mass_train[mass_train['image file path'].str.contains(dicom_row)])
            pass
    
    
    if laterality not in {"LEFT", "RIGHT"}:
        print(f"Error: Invalid laterality '{laterality}'")
    
    if view not in {"MLO", "CC"}:
        print(f"Error: Invalid view '{view}'")

    if dataset_type == "Mass-Training":
        if patient_id not in mass_train["patient_id"].values:
            print(f"Error: Patient {patient_id} not in {dataset_type}")
        else:
            patient_entries = mass_train[(mass_train == patient_id).any(axis=1)]
            patient_entries=patient_entries[(patient_entries == laterality).any(axis=1)]
            patient_entries=patient_entries[(patient_entries == view).any(axis=1)]
            for _, row in patient_entries.iterrows():
                pathology = row['pathology']
                if pathology == "BENIGN_WITHOUT_CALLBACK":
                    pathology = "BENIGN"
                data_to_save.append([image_path, pathology])
            count += len(patient_entries)

    if dataset_type == "Mass-Test":
        if patient_id not in mass_test["patient_id"].values:
            print(f"Error: Patient {patient_id} not in {dataset_type}")
        else:
            patient_entries = mass_test[(mass_test == patient_id).any(axis=1)]
            patient_entries=patient_entries[(patient_entries == laterality).any(axis=1)]
            patient_entries=patient_entries[(patient_entries == view).any(axis=1)]
            for _, row in patient_entries.iterrows():
                pathology = row['pathology']
                if pathology == "benign without callback":
                    pathology = "benign"
                data_to_save.append([image_path, pathology])
            count += len(patient_entries)

    
    # if dataset_type == "Calc-Training":
    #     if patient_id not in calc_train["patient_id"].values:
    #         print(f"Error: Patient {patient_id} not in {dataset_type}")
    #     else:
    #         patient_entries = calc_train[(calc_train == patient_id).any(axis=1)]
    #         patient_entries=patient_entries[(patient_entries == laterality).any(axis=1)]
    #         print(patient_entries)
    return count




# At this point, dicom_train looks like a 2D array
# Format: [[PatientID_1, image_path_1, series_description_1], [PatientID_2, image_path_2, series_description_2]]
data_to_save = []
count = 0 
for i in range(len(dicom_train)):
    count = ID_to_patient(dicom_train[i], count, data_to_save)

for i in range(len(dicom_test)):
    count = ID_to_patient(dicom_test[i], count, data_to_save)

print()
print(count)


print(data_to_save)


# Saving to CSV
with open('original_paths.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image_path', 'pathology'])
    writer.writerows(data_to_save)