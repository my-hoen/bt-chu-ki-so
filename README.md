# bt-chu-ki-so
- Ứng dụng Flask cho phép người dùng:
Tạo cặp khóa RSA (private/public)
Ký file bằng khóa riêng (private key)
Xác minh chữ ký với khóa công khai (public key)
- Công nghệ sử dụng
Python 3.x
Flask
Thư viện cryptography của Python
Cấu trúc thư mục
project/
│
├── app.py                
├── templates/
│   ├── index.html        
│   ├── sign.html         
│   ├── verify.html        
│   └── result.html        
├── keys/                  
├── uploads/              
└── README.md             
Cài đặt và chạy ứng dụng
- Tạo môi trường ảo (tùy chọn):
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate     # Trên Windows
- Cài đặt thư viện:
pip install Flask cryptography
- Chạy ứng dụng:
python app.py
- Truy cập trình duyệt:
http://172.16.21.49:5000  
![image](https://github.com/user-attachments/assets/0a23facf-81a8-45c0-ae1a-c6872c782982)
![image](https://github.com/user-attachments/assets/fe3346fb-7c7d-4da6-8756-95a9f968b843)


