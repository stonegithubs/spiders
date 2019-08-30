import pytesseract
from PIL import Image

image = Image.open('/home/zhang/temp.png')
text = pytesseract.image_to_string(image)

print(text)
