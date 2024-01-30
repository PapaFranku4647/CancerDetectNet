# Dim
# Make brighter
# Add noise
# Flip 90 degrees (Can be repeated multiple times)
# Mirror Vertically
# Mirror Horizontally

import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
import random

def adjust_brightness(image, brighter=True):
    factor = random.uniform(1.0, 1.0) if brighter else random.uniform(0.5, 1.0)
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def add_noise(image, noise_intensity=0.02):
    # noise_intensity = random.random()/20
    image_array = np.array(image)
    noise = np.random.randint(0, 256, image_array.shape, dtype=np.uint8)
    noise = (noise_intensity * noise).astype(np.uint8)
    noisy_image_array = np.add(image_array, noise, out=image_array, casting="unsafe")
    return Image.fromarray(noisy_image_array)

def random_flip_mirror(image):
    if random.choice([True, False]):
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if random.choice([True, False]):
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    for _ in range(random.randint(0, 3)):
        image = image.rotate(90, expand=True)
    return image

def create_random_variation(image_path, output_path):
    try:
        image = Image.open(image_path)

        # Ensure the image is resized to 256x256 with nearest neighbor interpolation
        image = image.resize((256, 256), Image.NEAREST)

        # Randomly adjust brightness
        image = adjust_brightness(image, random.choice([True, False]))

        # Randomly add noise
        if random.choice([True, False]):
            image = add_noise(image)

        # Randomly apply flip/mirror transformations
        image = random_flip_mirror(image)

        # Resize back to 256x256 if needed
        if image.size != (256, 256):
            image = image.resize((256, 256), Image.NEAREST)

        # Save the image in PNG format
        image.save(output_path, format='PNG')

    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def process_folders(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png')):
            input_image_path = os.path.join(input_folder, filename)
            for i in range(32):
                output_filename = f'{filename.split(".")[0]}_{i}.png'
                output_path = os.path.join(output_folder, output_filename)
                create_random_variation(input_image_path, output_path)


input_folder  = '-----------------\png'  # Replace with the path to your folder
output_folder = 'MIAS'
process_folders(input_folder, output_folder)


