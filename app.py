import streamlit as st
from streamlit_sortables import sort_items
from merger import merge_pdfs
from compressor import compress_pdf
import tempfile
import os

st.set_page_config(page_title="PDF Merger & Compressor", layout="centered")
st.title("📎 PDF Merger & Compressor")

action = st.radio("Choose an action:", ("Merge PDFs", "Compress a PDF", "Merge & Compress"))

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True if action != "Compress a PDF" else False
)

if uploaded_files:
    st.subheader("📄 Reorder PDFs by Drag & Drop")

    # List of uploaded file names
    file_names = [file.name for file in uploaded_files]
    
    # Drag-and-drop sort interface
    sorted_names = sort_items(file_names, direction="vertical")

    # sorted_names = sort_items(file_names, direction="vertical", label="Drag to reorder:")

    # Map filenames to uploaded file objects
    name_to_file = {file.name: file for file in uploaded_files}

    if st.button("Process PDFs"):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save uploaded files to temporary folder
            path_map = {}
            for name in sorted_names:
                file = name_to_file[name]
                file_path = os.path.join(tmpdir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.read())
                path_map[name] = file_path

            ordered_paths = [path_map[name] for name in sorted_names]

            result_path = ""

            if action == "Merge PDFs":
                result_path = os.path.join(tmpdir, "merged.pdf")
                merge_pdfs(ordered_paths, result_path)

            elif action == "Compress a PDF":
                result_path = os.path.join(tmpdir, "compressed.pdf")
                compress_pdf(ordered_paths[0], result_path)

            elif action == "Merge & Compress":
                merged_path = os.path.join(tmpdir, "merged.pdf")
                result_path = os.path.join(tmpdir, "merged_compressed.pdf")
                merge_pdfs(ordered_paths, merged_path)
                compress_pdf(merged_path, result_path)

            with open(result_path, "rb") as f:
                st.download_button("📥 Download Result", f, file_name=os.path.basename(result_path))
