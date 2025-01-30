from flask import Flask, request, send_file, render_template
import qrcode
from io import BytesIO

app = Flask(__name__)

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

    # Save the QR code to a BytesIO buffer instead of a file
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.route('/download_qr', methods=['GET'])
def download_qr():
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

    # Save the QR code to a BytesIO buffer for download
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, as_attachment=True, download_name="qr_code.png", mimetype='image/png')

# Use this for local development, though Vercel will handle the ASGI server
if __name__ == '__main__':
    app.run(debug=True)
