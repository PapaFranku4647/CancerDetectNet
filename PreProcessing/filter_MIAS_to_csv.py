import csv

with open("MIAS/KeyMap.txt") as key_map:
    lines = key_map.readlines()

data = []

for line in lines:
    parts = line.split(" ")
    image_file = parts[0]
    tissue_type = parts[1]
    abnormal = parts[2]

    if not abnormal == "CALC":
        if abnormal != "NORM":
            abnormal = parts[3].strip()

        if abnormal not in {"NORM", "M", "B"}:
            print(abnormal)
        
        if abnormal == "NORM":
            abnormal = "NORMAL"
        elif abnormal == "M":
            abnormal = "MALIGNANT"
        elif abnormal == "B":
            abnormal = "BENIGN"
        print(line)
        data.append([f"MIAS/{image_file}.pgm", abnormal])


with open('MIAS_Trimmed/csv/original_paths.csv', 'w', newline='') as original_csv:
    writer = csv.writer(original_csv)
    field = ["image_path", "pathology"]
    writer.writerow(field)
    writer.writerows(data)

