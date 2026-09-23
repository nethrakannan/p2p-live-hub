from flask import Flask, render_template, send_from_directory, request, redirect, url_for, abort
import os

app = Flask(__name__)

# CONFIGURATION
BASE_DIR = './shared_files'

@app.route('/')
def lobby():
    # Show the landing page first instead of auto-generating a random ID
    return render_template('lobby.html')

@app.route('/join', methods=['POST'])
def join_room():
    # Grab the custom room name typed by the user
    room_name = request.form.get('room_name', '').strip()
    if not room_name:
        return redirect(url_for('lobby'))
    
    # Sanitize the name so it doesn't cause folder errors (keeps only letters, numbers, hyphens)
    safe_room_name = "".join(x for x in room_name if x.isalnum() or x in ('-', '_'))
    
    # Send the user to their custom room URL
    return redirect(url_for('room_home', room_id=safe_room_name))

@app.route('/room/<room_id>')
def room_home(room_id):
    # Ensure folder structure exists for the custom room name
    room_id = "".join(x for x in room_id if x.isalnum() or x in ('-', '_'))
    room_dir = os.path.join(BASE_DIR, room_id)
    
    if not os.path.exists(room_dir):
        os.makedirs(room_dir)
        
    files = [f for f in os.listdir(room_dir) if os.path.isfile(os.path.join(room_dir, f))]
    return render_template('index.html', room_id=room_id, files=files)

@app.route('/room/<room_id>/upload', methods=['POST'])
def upload_file(room_id):
    room_id = "".join(x for x in room_id if x.isalnum() or x in ('-', '_'))
    room_dir = os.path.join(BASE_DIR, room_id)
    
    if 'file' not in request.files:
        return redirect(url_for('room_home', room_id=room_id))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('room_home', room_id=room_id))
    
    if file:
        file.save(os.path.join(room_dir, file.filename))
        return redirect(url_for('room_home', room_id=room_id))

@app.route('/room/<room_id>/download/<filename>')
def download_file(room_id, filename):
    room_id = "".join(x for x in room_id if x.isalnum() or x in ('-', '_'))
    room_dir = os.path.join(BASE_DIR, room_id)
    try:
        return send_from_directory(room_dir, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/room/<room_id>/delete/<filename>')
def delete_file(room_id, filename):
    room_id = "".join(x for x in room_id if x.isalnum() or x in ('-', '_'))
    room_dir = os.path.join(BASE_DIR, room_id)
    file_path = os.path.join(room_dir, filename)
    try:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
        return redirect(url_for('room_home', room_id=room_id))
    except Exception:
        abort(500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
