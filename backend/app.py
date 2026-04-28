"""
Flask Backend for AI Image Restoration Web Application.
Handles image upload, processing dispatch, and result delivery.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import time
import uuid

# Add parent directory to path so we can import the model module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.processor import process_image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Image Restoration API is running'})


@app.route('/api/restore', methods=['POST'])
def restore():
    """
    Accept an image upload and restoration type, process it,
    and return metadata including the output file ID.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    restoration_type = request.form.get('type', 'denoise')
    if restoration_type not in ['denoise', 'deblur', 'super_resolution']:
        return jsonify({'error': 'Invalid restoration type. Choose: denoise, deblur, super_resolution'}), 400

    # Save uploaded file with unique ID
    file_id = str(uuid.uuid4())
    ext = file.filename.rsplit('.', 1)[1].lower()
    input_filename = f'{file_id}_input.{ext}'
    output_filename = f'{file_id}_output.png'

    input_path = os.path.join(UPLOAD_FOLDER, input_filename)
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    try:
        start_time = time.time()
        method_used = process_image(input_path, output_path, restoration_type)
        processing_time = round(time.time() - start_time, 2)

        return jsonify({
            'success': True,
            'output_id': file_id,
            'processing_time': processing_time,
            'restoration_type': restoration_type,
            'method': method_used
        })
    except Exception as e:
        # Clean up input file on error
        if os.path.exists(input_path):
            os.remove(input_path)
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/api/image/<file_id>/<image_type>', methods=['GET'])
def get_image(file_id, image_type):
    """Serve an uploaded or processed image by its file ID."""
    if image_type == 'input':
        for f in os.listdir(UPLOAD_FOLDER):
            if f.startswith(file_id):
                return send_file(
                    os.path.join(UPLOAD_FOLDER, f),
                    mimetype='image/png'
                )
        return jsonify({'error': 'Input image not found'}), 404

    elif image_type == 'output':
        output_path = os.path.join(OUTPUT_FOLDER, f'{file_id}_output.png')
        if os.path.exists(output_path):
            return send_file(output_path, mimetype='image/png')
        return jsonify({'error': 'Output image not found'}), 404

    return jsonify({'error': 'Invalid image type. Use "input" or "output"'}), 400


if __name__ == '__main__':
    print("=" * 50)
    print("  AI Image Restoration API Server")
    print("  Running on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
