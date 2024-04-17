from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

load_dotenv(find_dotenv())

# img2txt

def img2txt(url):
    image_to_text = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
    text = image_to_text(url)
    print(text)
img2txt("img.jpg")