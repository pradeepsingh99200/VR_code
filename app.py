from flask import Flask, request, send_file, render_template
import qrcode
import os
from waitress import serve  # Production WSGI server

app = Flask(__name__)

# Folder to save QR codes
QR_FOLDER = "static/qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', qr_code=None)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data', '')
    
    if not data:
        return "Error: No data provided!", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    qr_filename = f"qr_{hash(data)}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    img.save(qr_path)

    return render_template('index.html', qr_code=qr_filename)

@app.route('/download_qr/<filename>')
def download_qr(filename):
    return send_file(os.path.join(QR_FOLDER, filename), as_attachment=True)

def run():
    serve(app, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    run()
