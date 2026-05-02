import os, sys, subprocess
from pypdf import PdfWriter
import fitz # PyMuPDF
from PIL import Image

def merge_pdfs(files, output_path, progress_callback=None):
    merger = PdfWriter()
    total = len(files)
    for i, pdf in enumerate(files):
        merger.append(pdf)
        if progress_callback:
            progress_callback((i + 1) / total)
    merger.write(output_path)
    merger.close()

def open_file(path):
    if sys.platform == "win32": os.startfile(path)
    elif sys.platform == "darwin": subprocess.call(["open", path])
    else: subprocess.call(["xdg-open", path])

def get_page_thumbnails(pdf_path, width=150):
        doc = fitz.open(pdf_path)
        thumbnails = []

        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(width / page.rect.width, width / page.rect.width))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            thumbnails.append(img)
        
        doc.close()
        return thumbnails