import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ExifTags, ImageDraw

def calculate_distances(image_path, output_image_path):
    # Open the original image
    original_image = Image.open(image_path)

    # Get the image's EXIF data to check for rotation information
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(original_image._getexif().items())
        if exif[orientation] == 3:
            original_image = original_image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            original_image = original_image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            original_image = original_image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No EXIF data, or the data does not contain orientation information
        pass

    width, height = original_image.size

    # Load the pixel data
    original_pixels = original_image.load()

    # Create a new image for drawing arrows
    arrows_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(arrows_image)

    # Specify the y-coordinates where distances will be calculated
    y_positions = [int(height / 2)]

    # Iterate through each y-axis position in the image
    for y in y_positions:
        # Calculate the distance between consecutive pixels on the x-axis
        x_distances = [abs(original_pixels[x, y][0] - original_pixels[x + 1, y][0]) for x in range(width - 1)]

        # Draw red dots at specific y-coordinates
        draw.point((width // 2, y), fill="red")

        # Draw blue arrows representing x-axis distances
        for x, distance in enumerate(x_distances):
            # Adjust the arrow size and thickness
            arrow_size = int(distance / 5)
            arrow_thickness = max(1, int(distance / 20))
            
            # Calculate arrowhead points
            arrowhead = [(x + 1, y), (x + 1 - arrow_size, y - arrow_size), (x + 1 - arrow_size, y + arrow_size)]
            
            # Draw the arrow line
            draw.line([(x, y), (x + 1, y)], fill="blue", width=arrow_thickness)
            
            # Draw the arrowhead
            draw.polygon(arrowhead, fill="blue")

    # Save the arrows image
    arrows_image.save(output_image_path)

def calculate_distances_and_draw_arrows(image_path):
    # Ask the user for the output image path
    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if output_image_path:
        # Calculate distances and draw arrows on the output image
        calculate_distances(image_path, output_image_path)
        messagebox.showinfo("Information", "Distances and arrows drawn on the output image.")

def open_image_and_draw_arrows():
    # Open a file dialog to choose an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

    if file_path:
        # Calculate distances and draw arrows on the output image
        calculate_distances_and_draw_arrows(file_path)

# Create the main window
main_window = tk.Tk()
main_window.title("Main Window")
main_window.geometry('300x100')

# Create a button to open the second GUI
open_second_gui_button = tk.Button(main_window, text="Open Second GUI", command=open_image_and_draw_arrows)
open_second_gui_button.pack(pady=10)

# Initialize global variables for the second GUI
second_gui_image_label = None
second_gui_tk_image = None

def process_and_display_image_second_gui(image_path):
    global second_gui_tk_image
    
    # Open the original image
    original_image = Image.open(image_path)
    
    # Convert the image to a format that Tkinter can use
    second_gui_tk_image = ImageTk.PhotoImage(original_image)

    # Update the Label with the new image
    second_gui_image_label.config(image=second_gui_tk_image)
    second_gui_image_label.image = second_gui_tk_image  # Keep a reference to prevent the image from being garbage collected

# Create the second GUI window
second_gui_window = tk.Toplevel(main_window)
second_gui_window.title("Second GUI")
second_gui_window.geometry('500x500')

# Create a Label widget to display the image in the second GUI
second_gui_image_label = tk.Label(second_gui_window)
second_gui_image_label.pack(pady=10)

# Start the Tkinter event loop for the main window
main_window.mainloop()
