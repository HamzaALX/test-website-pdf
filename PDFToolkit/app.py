import io
import zipfile
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import fitz  # PyMuPDF
import tempfile
from PyPDF2 import PdfFileMerger
from pdf2docx import Converter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MERGED_FOLDER'] = 'merged_pdfs'
app.secret_key = 'supersecretkey'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['MERGED_FOLDER']):
    os.makedirs(app.config['MERGED_FOLDER'])

def merge_pdfs(pdf_list, output_path):
    merger = PdfFileMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/merge')
def merge_page():
    return render_template('merge.html')

@app.route('/convert_to_jpg')
def convert_to_jpg_page():
    return render_template('convert_to_jpg.html')

@app.route('/convert_to_docx')
def convert_to_docx_page():
    return render_template('convert_to_docx.html')

@app.route('/merge', methods=['POST'])
def merge():
    if 'files' not in request.files:
        flash('No files part', 'error')
        return redirect(request.url)

    files = request.files.getlist('files')
    if not files:
        flash('No files uploaded', 'error')
        return redirect(request.url)

    pdf_list = []
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        pdf_list.append(file_path)

    if not pdf_list:
        flash('No valid PDF files uploaded', 'error')
        return redirect(request.url)

    output_path = os.path.join(app.config['MERGED_FOLDER'], 'merged.pdf')
    merge_pdfs(pdf_list, output_path)

    return send_file(output_path, as_attachment=True)

@app.route('/convert_to_jpg', methods=['POST'])
def convert_to_jpg():
    files = request.files.getlist('pdf_files')
    error_files = []
    converted_files = []

    with tempfile.TemporaryDirectory() as tempdir:
        for file in files:
            try:
                filepath = os.path.join(tempdir, file.filename)
                file.save(filepath)
                doc = fitz.open(filepath)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap()
                    output_filename = f"{os.path.splitext(file.filename)[0]}_page_{page_num + 1}.jpg"
                    output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                    pix.save(output_filepath)
                    converted_files.append(output_filepath)
                doc.close()
            except Exception as e:
                error_files.append(file.filename)
                print(f"Error processing {file.filename}: {e}")

        if error_files:
            flash(f"Failed to convert the following files: {', '.join(error_files)}", 'error')
        if converted_files:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for converted_file in converted_files:
                    zip_file.write(converted_file, os.path.basename(converted_file))
            zip_buffer.seek(0)
            return send_file(
                zip_buffer,
                as_attachment=True,
                mimetype='application/zip',
                download_name='converted_images.zip'
            )

    return redirect('/')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['pdf']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_path)

    docx_file = file_path.replace('.pdf', '.docx')
    cv = Converter(file_path)
    cv.convert(docx_file)
    cv.close()

    return send_file(docx_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
