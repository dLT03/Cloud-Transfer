from flask import Flask, request, send_from_directory, jsonify, render_template, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import socket
import os
import zipfile
import uuid

# initialize Flask app
app = Flask(__name__, static_folder="static", static_url_path='', template_folder="templates")
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

# Prometheus metrics
upload_counter = Counter('uploaded_files_total', 'Total number of uploaded files')
upload_size_total = Gauge('uploaded_file_size_total_bytes', 'Total size of uploaded files in bytes')
download_counter = Counter('downloaded_files_total', 'Total number of downloaded files', ['instance'])

@app.route('/upload', methods=['POST'])
def upload_file():
    custom_name = request.form.get("customName", "").strip()

    # Folder support (multiple files)
    if 'files' in request.files:
        files = request.files.getlist('files')
        folder_name = request.form.get("folderName", "folder")
        base_name = secure_filename(custom_name) if custom_name else secure_filename(folder_name)
        
        # Ensure the ZIP extension
        if not base_name.lower().endswith(".zip"):
            base_name += ".zip"
        zip_path = os.path.join(UPLOAD_FOLDER, base_name)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                rel_path = secure_filename(file.filename)
                zipf.writestr(rel_path, file.read())

        download_url = f"http://localhost/preview/{base_name}"
        
         # Update Prometheus metrics
        upload_size_total.inc(os.path.getsize(zip_path))
        upload_counter.inc()
        
        return jsonify({"message": "Folder zipped", "download_link": download_url})

    # Single file support
    if 'file' in request.files:
        file = request.files['file']
        original_name = secure_filename(file.filename)
        original_ext = os.path.splitext(original_name)[1]
        
        # Use custom name if provided, preserving file extension
        if custom_name:
            filename = secure_filename(custom_name)
            if not filename.lower().endswith(original_ext.lower()):
                filename += original_ext
        else:
            filename = original_name

        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        upload_size_total.inc(os.path.getsize(path))
        upload_counter.inc()
        download_url = f"http://localhost/preview/{filename}"
        return jsonify({"message": "Uploaded", "download_link": download_url})

    return "No file uploaded", 400

# Page for downloading files
@app.route('/preview/<filename>')
def download_page(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return render_template('download.html', filename=filename)
    else:
        return "File not found", 404

# Serve the actual file as an attachment
@app.route('/file/<filename>')
def serve_file(filename):
    download_counter.labels(instance=socket.gethostname()).inc()
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route('/')
def index():
    return app.send_static_file('index_front.html')

# run app on all interfaces
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
