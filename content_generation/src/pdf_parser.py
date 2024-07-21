import PyPDF2

def parse_pdf(pdf_file_path):
    content = ""
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text()
        return content

    except FileNotFoundError:
        print(f"File not found: {pdf_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
