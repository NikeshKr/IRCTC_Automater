from PIL import Image
import pytesseract

# Set the correct path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open an image file
img = Image.open('captcha.png')

# Use Tesseract to extract text
text = pytesseract.image_to_string(img)
print(text)
