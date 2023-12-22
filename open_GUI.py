import tkinter as tk
from PIL import Image, ImageTk  # Pillow library for working with images

def open_image():
    # Open an image file
    image_path = "output_image_range_check.jpeg"  # Replace with the path to your image
    original_image = Image.open(image_path)
    

    # Convert the image to a format that Tkinter can use
    tk_image = ImageTk.PhotoImage(original_image)

    # Update the Label with the new image
    image_label.config(image=tk_image)
    image_label.image = tk_image  # Keep a reference to prevent image from being garbage collected

# Create the main window
window = tk.Tk()
window.title("Image Viewer")
window.geometry('300x300')
window.focus

# Create a Label widget to display the image
image_label = tk.Label(window)
image_label.pack(pady=10)

# Create a button to open the image
open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
