# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os
from pdf2image import convert_from_path


class PDFtoImage:
    """Takes a PDF and comvert to Image file"""
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def convert_to_image(self):
        pages = convert_from_path(self.pdf_path, 500)
        page_number = 1
        for page in pages:   
            # Declaring filename for each page of PDF as JPG 
            # For each page create an image file: 
        
            filename = self.pdf_path + "_page_"+str(page_number)+".jpg"
            # Save the image of the page in system 
            page.save(filename, 'JPEG') 
      
            # Increment for the page number
            page_number += 1




class ImageReader:
    """Take an input of Image Directory and loads on python"""
    def __init__(self, image_directory):
        """load or show the Imagefile"""
        self.image_directory = image_directory
        self.image = self.load_image_PIL()

    def load_image_PIL(self):
        """load image file"""
        img = Image.open(self.image_directory)
        
        return img

    def show_image(self):
        """show image"""
        self.image.show()

class ExtractText ():
    """Extract text out of image"""
    def __init__(self, image):
        self.image = image

    def extract_text(self):
        """Extract text from an image using tesseract"""
        text = pytesseract.image_to_string(self.image)
        # print(text)
        return text


if __name__ == "__main__":
    test_pdf = PDFtoImage("./img/3134.pdf")
    test_pdf.convert_to_image() 
    test_image = ImageReader("./img/page_1.jpg")
    # test_image.show_image()
    text = ExtractText(test_image.image)
    print(text.extract_text())