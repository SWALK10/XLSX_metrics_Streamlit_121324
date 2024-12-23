from PIL import Image
import os

def resize_gif(input_path, output_path, reduction_percent):
    # Open the GIF
    img = Image.open(input_path)
    
    # Get original size
    width, height = img.size
    
    # Calculate new size (50% reduction)
    new_width = int(width * (reduction_percent / 100))
    new_height = int(height * (reduction_percent / 100))
    
    # Resize the image while maintaining aspect ratio
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save the resized image
    img.save(output_path, 'GIF')
    print(f"Resized from {width}x{height} to {new_width}x{new_height} pixels")

if __name__ == "__main__":
    input_file = "Logo_Final2.gif"
    output_file = "Logo_Final2_50pct.gif"
    
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_path = os.path.join(current_dir, input_file)
    output_path = os.path.join(current_dir, output_file)
    
    # Resize to 50% of original size
    resize_gif(input_path, output_path, 50)
