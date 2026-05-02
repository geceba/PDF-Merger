import os, sys, subprocess
from pypdf import PdfWriter, PdfReader
import fitz # PyMuPDF
from PIL import Image

def merge_pdfs(files_list, pdf_configs, output_path, progress_callback=None):
    writer = PdfWriter()
    total = len(pdf_configs)

    for i, path in enumerate(files_list):
        if path in pdf_configs:
            config = pdf_configs[path]
            reader = PdfReader(path)
            
            for page_idx in config['order']:
                if page_idx not in config['excluded']:
                    writer.add_page(reader.pages[page_idx])
        
        if progress_callback:
            progress_callback((i + 1) / total)
    
    with open(output_path, "wb") as f:
        writer.write(f)
    writer.close()

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