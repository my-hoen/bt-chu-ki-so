# Secure File Transfer Application

This project is a secure file transfer application that allows users to create RSA key pairs, sign files, and verify signatures using a web interface built with Flask.

## Project Structure

```
secure_file_transfer
├── app.py                # Main application logic using Flask
├── templates             # HTML templates for the web application
│   ├── index.html       # Homepage with links to functionalities
│   ├── sign.html        # Form for signing files
│   ├── verify.html      # Form for verifying signatures
│   └── result.html      # Displays results of signature verification
├── keys                  # Directory for storing RSA key pairs
├── requirements.txt      # Lists project dependencies
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd secure_file_transfer
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the following command to start the Flask application:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage Guidelines

- **Create RSA Key Pair**: Navigate to the homepage and click on the link to create a new RSA key pair. This will generate a private and public key stored in the `keys` directory.

- **Sign a File**: Use the sign functionality to upload a file you wish to sign. The application will generate a signature and save it as `signature.sig`.

- **Verify a Signature**: To verify a signature, upload the original file and its corresponding signature. The application will check the validity of the signature and display the result.

## Dependencies

- Flask
- cryptography

Make sure to check the `requirements.txt` file for the specific versions of the dependencies used in this project.