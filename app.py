from flask import Flask, render_template, send_from_directory, request, redirect, url_for, abort
import os

app = Flask(__name__)

# CONFIGURATION
SHARED_DIR = './shared_files'

# Ensure the shared directory exists
if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR)

@app.route('/')
def home():
    # Automatically scan the folder to list available files
    files = [f for f in os.listdir(SHARED_DIR) if os.path.isfile(os.path.join(SHARED_DIR, f))]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle incoming files sent from the website interface
    if 'file' not in request.files:
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))
    
    if file:
        # Save the uploaded file directly into the shared folder
        file.save(os.path.join(SHARED_DIR, file.filename))
        return redirect(url_for('home'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(SHARED_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
