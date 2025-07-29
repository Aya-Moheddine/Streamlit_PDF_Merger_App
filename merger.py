from pypdf import PdfReader, PdfWriter

def merge_pdfs(pdf_paths, output_path):
    """
    Merge multiple PDF files into a single PDF.

    Args:
        pdf_paths (list of str): List of paths to PDF files to merge.
        output_path (str): Path to save the merged PDF.
    """
    writer = PdfWriter()

    for pdf_file in pdf_paths:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as f_out:
        writer.write(f_out)

    print(f"PDF merged successfully {output_path}")
