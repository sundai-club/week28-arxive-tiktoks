import PyPDF2
import scipdf


def get_all_images(pdf_file_path):
    scipdf.parse_figures(pdf_file_path, output_folder=pdf_file_path.split('.pdf')[0] + '_figures')
    return pdf_file_path.split('.pdf')[0] + '_figures'


def parse_pdf(pdf_file_path):
    content = ""
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text()

        images_path = get_all_images(pdf_file_path)
        return content, images_path

    except FileNotFoundError:
        print(f"File not found: {pdf_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
