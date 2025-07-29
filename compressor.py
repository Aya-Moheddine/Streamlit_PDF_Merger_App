import fitz 
from PIL import Image
import io

# this function compresses the image to reduce its quality. 

def compress_pdf(input_path, output_path, zoom=1.0, image_quality=60):
    pdf = fitz.open(input_path)
    new_pdf = fitz.open()

    for page in pdf:
        # Render page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Compress image to JPEG in memory
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG", quality=image_quality)
        img_bytes.seek(0)

        # Create new blank page and insert image
        img_rect = fitz.Rect(0, 0, pix.width, pix.height)
        page_pdf = new_pdf.new_page(width=pix.width, height=pix.height)
        page_pdf.insert_image(img_rect, stream=img_bytes.getvalue())

    new_pdf.save(output_path)
    pdf.close()
    new_pdf.close()
    print(f"✅ Compressed PDF saved to: {output_path}")
