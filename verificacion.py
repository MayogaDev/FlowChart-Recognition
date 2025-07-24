import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print("Tesseract OCR path set to:", pytesseract.pytesseract.tesseract_cmd)