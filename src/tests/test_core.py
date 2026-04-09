from pypdf import PdfWriter
from core.pdf_engine import merge_pdfs

def create_dummy_pdf(path):
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)

def test_merge_pdfs(tmp_path):
    pdf_one = tmp_path / "one.pdf"
    pdf_two = tmp_path / "two.pdf"
    output_pdf = tmp_path / "output.pdf"

    create_dummy_pdf(pdf_one)
    create_dummy_pdf(pdf_two)
    files = [str(pdf_one), str(pdf_two)]
    merge_pdfs(files, output_pdf)

    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0

def test_merge_pdfs_progress(tmp_path):
    pdf1 = tmp_path / "1.pdf"
    output = tmp_path / "out.pdf"
    create_dummy_pdf(pdf1)

    progress_values = []
    def callback(val):
        progress_values.append(val)

    merge_pdfs([str(pdf1)], str(output), progress_callback=callback)
    assert 1.0 in progress_values
