import PyPDF2
import os.path as op
import os
import subprocess
import tempfile
import shutil

PDF_FIGURES_JAR_PATH = 'pdffigures2/pdffigures2-assembly-0.0.12-SNAPSHOT.jar'

print(os.path.abspath(PDF_FIGURES_JAR_PATH))


def parse_figures(pdf_file, jar_path, output_folder, resolution=300):

    #if not op.isdir(output_folder):
    shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    data_path = op.join(output_folder, "data")
    figure_path = op.join(output_folder, "figures")
    if not op.exists(data_path):
        os.makedirs(data_path)
    if not op.exists(figure_path):
        os.makedirs(figure_path)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_pdf_path = op.join(temp_dir, op.basename(pdf_file))

        # Copy the PDF file to the temporary directory
        shutil.copy(pdf_file, temp_pdf_path)
        if op.isdir(data_path) and op.isdir(figure_path):
            args = [
                "java",
                "-jar",
                jar_path,
                temp_pdf_path,
                "-i",
                str(resolution),
                "-d",
                op.join(op.abspath(data_path), ""),
                "-m",
                op.join(op.abspath(figure_path), ""),
            ]
            _ = subprocess.run(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60
            )
            print(_)
            print('extracted images')
            return True
    return False



def get_all_images(pdf_file_path):
    output_folder = 'current_outputs'
    if not parse_figures(pdf_file_path, PDF_FIGURES_JAR_PATH, output_folder):
        return None
    return output_folder


def parse_pdf(pdf_file_path):

    

    content = ""
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print('Parsed PDF')
            for page in pdf_reader.pages:
                content += page.extract_text() 

        return content

    except FileNotFoundError:
        print(f"File not found: {pdf_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
