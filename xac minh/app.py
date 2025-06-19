from flask import Flask, request, render_template, redirect, url_for, flash, send_file, send_from_directory
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

app = Flask(__name__)
app.secret_key = 'your_secret_key'
KEY_DIR = "keys"
os.makedirs(KEY_DIR, exist_ok=True)

def create_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(f"{KEY_DIR}/private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    public_key = private_key.public_key()
    with open(f"{KEY_DIR}/public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def sign_file(file_path):
    with open(f"{KEY_DIR}/private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open(file_path, "rb") as f:
        file_data = f.read()

    signature = private_key.sign(
        file_data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    with open("signature.sig", "wb") as f:
        f.write(signature)

def verify_signature(file_path, signature_path, public_key_path):
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    with open(file_path, "rb") as f:
        file_data = f.read()

    with open(signature_path, "rb") as f:
        signature = f.read()

    try:
        public_key.verify(
            signature,
            file_data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_keys', methods=['POST'])
def create_keys_route():
    create_keys()
    # Sau khi tạo, trả về file zip chứa cả 2 key
    import zipfile
    zip_path = os.path.join(KEY_DIR, "rsa_keys.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(os.path.join(KEY_DIR, "private_key.pem"), "private_key.pem")
        zipf.write(os.path.join(KEY_DIR, "public_key.pem"), "public_key.pem")
    return send_file(zip_path, as_attachment=True)

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            os.makedirs('uploads', exist_ok=True)
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            signature_path = os.path.join('uploads', file.filename + '.sig')
            # Ký file và lưu chữ ký vào signature_path
            with open(f"{KEY_DIR}/private_key.pem", "rb") as f:
                private_key = serialization.load_pem_private_key(f.read(), password=None)
            with open(file_path, "rb") as f:
                file_data = f.read()
            signature = private_key.sign(
                file_data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            with open(signature_path, "wb") as f:
                f.write(signature)
            # Cho phép tải file chữ ký về
            return send_file(signature_path, as_attachment=True)
    return render_template('sign.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        file = request.files['file']
        signature = request.files['signature']
        public_key = request.files['public_key']
        if file and signature and public_key:
            os.makedirs('uploads', exist_ok=True)
            file_path = os.path.join('uploads', file.filename)
            signature_path = os.path.join('uploads', signature.filename)
            public_key_path = os.path.join('uploads', public_key.filename)
            file.save(file_path)
            signature.save(signature_path)
            public_key.save(public_key_path)
            is_valid = verify_signature(file_path, signature_path, public_key_path)
            return render_template('result.html', is_valid=is_valid)
    return render_template('verify.html')

if __name__ == "__main__":
    app.run(debug=True)