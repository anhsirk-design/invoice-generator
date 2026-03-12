from docx2pdf import convert
import pythoncom


def convert_to_pdf(docx_path):

    pythoncom.CoInitialize()

    pdf_path = docx_path.replace(".docx", ".pdf")

    convert(docx_path, pdf_path)

    pythoncom.CoUninitialize()

    return pdf_path