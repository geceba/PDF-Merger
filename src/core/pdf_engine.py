import os, sys, subprocess
from pypdf import PdfWriter

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