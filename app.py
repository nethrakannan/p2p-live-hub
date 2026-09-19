from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__)

# CONFIGURATION
# Using 0.0.0.0 makes the website available to any device connected to your hotspot!
HOST = '0.0.0.0'  
PORT = 5000       
SHARED_DIR = './shared_files'

@app.route('/')
def home():
    # Automatically scan the folder to see what files are available to share
    if os.path.exists(SHARED_DIR):
        files = [f for f in os.listdir(SHARED_DIR) if os.path.isfile(os.path.join(SHARED_DIR, f))]
    else:
        files = []
    
    # Send the file list over to the website UI
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    # Safely handle the P2P file transfer when the user clicks 'Download'
    try:
        return send_from_directory(SHARED_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    # Render tells our app what port to use via an environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
