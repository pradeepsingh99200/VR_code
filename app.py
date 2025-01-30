from flask import Flask, request, send_file, render_template
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', qr_code=None)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data', '')
    
    if not data:
        return "Error: No data provided!", 400

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Save the QR code to a BytesIO buffer
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Convert the image to base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template('index.html', qr_code=img_base64, qr_data=data)

@app.route('/download_qr', methods=['GET'])
def download_qr():
    data = request.args.get('data', '')
    
    if not data:
        return "Error: No data provided!", 400

    # Generate QR code for download
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
