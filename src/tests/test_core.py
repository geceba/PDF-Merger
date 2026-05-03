import pytest
from pypdf import PdfWriter, PdfReader
from core.pdf_engine import merge_pdfs

def create_dummy_pdf(path, pages=1):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)

def test_merge_pdfs_with_config(tmp_path):
    pdf_one = tmp_path / "one.pdf"
    output_pdf = tmp_path / "output.pdf"
    
    create_dummy_pdf(pdf_one, pages=3)
    files_list = [str(pdf_one)]
    
    configs = {
        str(pdf_one): {
            "order": [2, 1, 0], 
            "excluded": {1}
        }
    }
    
    merge_pdfs(files_list, configs, str(output_pdf))

    assert output_pdf.exists()
    
    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 2

def test_merge_pdfs_progress(tmp_path):
    pdf1 = tmp_path / "1.pdf"
    pdf2 = tmp_path / "2.pdf"
    output = tmp_path / "out.pdf"
    
    create_dummy_pdf(pdf1)
    create_dummy_pdf(pdf2)

    files_list = [str(pdf1), str(pdf2)]
    configs = {
        str(pdf1): {"order": [0], "excluded": set()},
        str(pdf2): {"order": [0], "excluded": set()}
    }

    progress_values = []
    def callback(val):
        progress_values.append(val)

    merge_pdfs(files_list, configs, str(output), progress_callback=callback)
    
    assert 1.0 in progress_values
    assert len(progress_values) >= 2