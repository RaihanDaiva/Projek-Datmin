from flask import Flask, send_from_directory, jsonify
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

@app.route('/documents')
def list_documents():
    files = []
    for fname in os.listdir(UPLOAD_FOLDER):
        fpath = os.path.join(UPLOAD_FOLDER, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1]
            files.append({
                "id": fname,
                "name": fname,
                "type": ext,
                "status": "Available"
            })
    return jsonify(files)

@app.route('/documents/<filename>')
def get_document(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=False
    )

if __name__ == '__main__':
    app.run(debug=True)