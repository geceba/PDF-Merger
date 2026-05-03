import fitz
from pdf2docx import Converter
from src.utils.i18n import TEXTS
import os

class DocEngine:
    @staticmethod
    def convert_pdf_to_word(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            is_scanned = True
            for page in doc:
                if len(page.get_text().strip()) > 20:
                    is_scanned = False
                    break
            doc.close()

            if is_scanned:
                return False, TEXTS['msg_conversion_error']

            output_path = os.path.splitext(pdf_path)[0] + ".docx"

            cv = Converter(pdf_path)
            cv.convert(output_path)
            cv.close()

            return True, output_path

        except Exception as e:
            return False, str(e)