## Must be run from base directory BreastCancerNetwork

# Filter out pandas depreciation warning
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import packages
import csv
import os
import pandas as pd
from PIL import Image



#### Save the PNGs ####
# Load the CSV file
df = pd.read_csv('INbreast_Trimmed/csv/original_filtered.csv')

# Define the new image directory
new_img_dir = 'INbreast_Trimmed/png'

# List to store new image paths and pathology
image_data = []

# Create the directory if it doesn't exist
if not os.path.exists(new_img_dir):
    os.makedirs(new_img_dir)

# Iterate over the rows in the DataFrame
for index, row in df.iterrows():
    original_image_path = row['JPEG Path']
    pathology = row['Pathology']  # Assuming 'pathology' is the column name in your CSV
    new_filename = f"{new_img_dir}/{index}.png"
    image_data.append([new_filename, pathology])

    # Load and process the image
    try:
        with Image.open(original_image_path) as img:
            # Convert to grayscale and resize using nearest neighbor interpolation
            img = img.convert('L').resize((256, 256), Image.NEAREST)

            # Save the image with the new filename in PNG format
            img.save(new_filename, 'PNG')
    except IOError:
        print(f"Error in loading image at {original_image_path}")

# Save the new image paths and pathology to a CSV file
new_csv_path = 'INbreast_Trimmed/csv/png_paths.csv'
with open(new_csv_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image_path', 'pathology'])
    for data in image_data:
        writer.writerow(data)

print(f"New image data saved to {new_csv_path}")
