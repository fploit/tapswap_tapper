import json
import requests
import os
from PIL import Image
import cv2
import pytesseract

config = json.loads(open("./config.json", "r").read())



def resize_image(image_path, max_size_kb=1024):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the current size in bytes
        current_size = os.path.getsize(image_path)
        # Convert to KB
        current_size_kb = current_size / 1024
        
        # Resize if the image is larger than max_size_kb
        if current_size_kb > max_size_kb:
            # Calculate the reduction factor
            reduction_factor = (max_size_kb / current_size_kb) ** 0.5
            new_width = int(img.width * reduction_factor)
            new_height = int(img.height * reduction_factor)
            
            # Resize the image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save the resized image to a new file
            resized_image_path =  os.path.basename(image_path)
            img.save(resized_image_path, optimize=True, quality=85)
            
            return resized_image_path
        else:
            return image_path


def check_text_in_image(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    has_digit = any(char.isdigit() for char in text)
    has_alpha = any(char.isalpha() for char in text)

    return has_digit, has_alpha


def png_to_text(file_path):
    try:
        api_key = config['ocr_api_key']
        url = "https://api8.ocr.space/parse/image"

        file_path = resize_image(file_path)

        payload = {
            "language": "eng",
            "isOverlayRequired": True,
            "FileType": ".Auto",
            "IsCreateSearchablePDF": False,
            "isSearchablePdfHideTextLayer": True,
            "detectOrientation": False,
            "isTable": False,
            "scale": True,
            "OCREngine": 1,
            "detectCheckbox": False,
            "checkboxTemplate": 0
        }

        with open(file_path, 'rb') as file:
            files = {
                'file': (file_path, file, 'image/png')
            }
            headers = {
                'apikey': api_key
            }
            response = requests.post(url, headers=headers, data=payload, files=files)

        return response.json()['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText']
    except:
        return "0"


def check_photo():
    photo_path = './code.png'
    has_digit, has_alpha = check_text_in_image(photo_path)
    print(f"Contains digits: {has_digit}")
    print(f"Contains letters: {has_alpha}")
    if has_alpha or has_digit:
        return png_to_text(photo_path)
    else:
        return "0"

