import tkinter as tk 
from tkinter import filedialog
from PIL import Image
import os
from reportlab.pdfgen import canvas 
import random as rn

class Image2Pdf:
    def __init__(self, root):
        # Initialize the Image2Pdf class with the given Tkinter root window
        self.root = root
        self.image_path = []  # List to store selected image paths
        self.output_pdf_name = tk.StringVar()  # Variable to store the output PDF name
        self.selected_images = tk.Listbox(root, selectmode=tk.MULTIPLE)  # Listbox to display selected image filenames
        self.ini_ui()  # Initialize the user interface

    def ini_ui(self):
        # Set up the user interface
        title = tk.Label(self.root, text="Image to Pdf", font=("Arial", 20, "bold"))
        title.pack(pady=(0, 0))

        but1 = tk.Button(self.root, text="Select Images", background="grey", command=self.select_images, font=("Arial", 10))
        but1.pack(pady=(10, 20))

        self.selected_images.pack(pady=0, fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter Pdf Name:")
        label.pack()

        name_pdf = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify="center")
        name_pdf.pack() 

        but2 = tk.Button(self.root, text="Convert", background="grey", command=self.convert_img2pdf, font=("Arial", 10))
        but2.pack(pady=(10, 20))

    def select_images(self):
        # Open a file dialog to allow the user to select multiple image files
        self.image_path = filedialog.askopenfilenames(title="Select Images")
        self.update_selected_images()  # Update the displayed image filenames in the Listbox

    def update_selected_images(self):
        # Update the Listbox with selected image filenames
        for imag_path in self.image_path:
            _, imag_path = os.path.split(imag_path)
            self.selected_images.insert(tk.END, imag_path)

    def convert_img2pdf(self):
        if not self.image_path:
            return  # If no images selected, exit the function

        # Determine the output PDF path based on user input or generate a random name
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else f"pdf{rn.randint(0, 99999)}.pdf"
        
        # Create a PDF canvas
        pdf = canvas.Canvas(output_pdf_path)

        for img_path in self.image_path:
            # Open each image
            img = Image.open(img_path)
            
            # Set canvas fill color to white
            pdf.setFillColorRGB(255, 255, 255)
            
            # Draw a white-filled rectangle to cover the entire page
            pdf.rect(0, 0, 612, 792, fill=True)
            
            # Calculate dimensions and position for drawing the image on the page
            a_width = 540
            a_height = 720
            scale_factor = min(a_width / img.width, a_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_cen = (612 - new_width) / 2
            y_cen = (792 - new_height) / 2
            
            # Draw the image on the PDF canvas
            pdf.drawInlineImage(img, x_cen, y_cen, width=new_width, height=new_height)
            
            # Move to the next page in the PDF
            pdf.showPage()

        # Save the PDF
        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image2Pdf")
    Image2Pdf(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()
