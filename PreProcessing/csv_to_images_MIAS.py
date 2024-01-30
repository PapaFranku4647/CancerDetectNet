import csv
import pandas as pd
from PIL import Image
import os


original_paths_csv = pd.read_csv("MIAS_Trimmed/csv/original_paths.csv")



new_img_dir = 'MIAS_Trimmed/png'

image_data = []

if not os.path.exists(new_img_dir):
    os.makedirs(new_img_dir)


for index, row in original_paths_csv.iterrows():
    original_image_path = row['image_path']
    pathology = row['pathology']
    new_filename = f"{new_img_dir}/{index}.png"
    image_data.append([new_filename, pathology])

    # Load and process the image
    try:
        with Image.open(original_image_path) as img:
            img = img.convert('L').resize((256, 256), Image.NEAREST)
            img.save(new_filename, 'PNG')
    except IOError:
        print(f"Error in loading image at {original_image_path}")

# Save the new image paths and pathology to a CSV file
new_csv_path = 'MIAS_Trimmed/csv/png_paths.csv'
with open(new_csv_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image_path', 'pathology'])
    for data in image_data:
        writer.writerow(data)

print(f"New image data saved to {new_csv_path}")