import os
import fitz  # PyMuPDF
from PIL import Image
import pillow_avif
def generate_pdf_thumbnails(input_folder, output_folder, thumbnail_size=(300, 300), cut=2.5):
    """
    Generate thumbnails for all PDFs in a folder, showing only the top 1/3 of the first page.
    
    Args:
        input_folder (str): Path to folder containing PDFs
        output_folder (str): Path to save thumbnails
        thumbnail_size (tuple): Desired thumbnail dimensions (width, height)
        cut (float): How much of the top portion to show (e.g., 2.5 means top 1/2.5 of the page)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each PDF in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.avif")
            
            try:
                # Open PDF
                doc = fitz.open(pdf_path)
                
                # Get first page
                page = doc.load_page(0)
                
                # Get the page's rectangle
                rect = page.rect
                
                # Calculate the top portion of the page
                top_portion = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 / cut)
                
                # Render only the top portion of the page (300 DPI for good quality)
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), clip=top_portion)
                
                # Convert to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Create thumbnail
                img.thumbnail(thumbnail_size)
                
                # Save as AVIF
                img.save(output_path, "AVIF", quality=80)
                
                print(f"Generated thumbnail for {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

# Example usage
generate_pdf_thumbnails(r"F:\all\GitHub\cristiank_website\public\sheet_music", r"F:\all\GitHub\cristiank_website\public\sheet_music\thumbnails")