import os
import json
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client 
from dotenv import load_dotenv

# Load biến môi trường để lấy KEY và URL
load_dotenv()

app = Flask(__name__)

# Khởi tạo kết nối tới Supabase
url: str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)

# Định tuyến cho trang chủ
@app.route('/')
def home():
    return render_template('index.html')

# Định tuyến cho trang slide
@app.route('/slide')
def slide():
    return render_template('slide.html')

@app.route('/api/save_contact', methods = ['POST'])
def save_contact():
    # Lấy dữ liệu từ JS gửi đến
    data = request.get_json()
    
    # Gửi lệnh Insert vào Supabase
    try:
        respone = supabase.table('mbf_contacts').insert(data).execute()
        
        # Kiểm tra dữ liệu có được lưu thành công không
        if respone.data:
            return jsonify({
                "message": "Lưu dữ liệu liên hệ thành công!",
                "status": "success"
            })
        else:
            return jsonify({
                "message": "Lưu dữ liệu liên hệ thất bại!",
                "status": "error"
            }), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500
    
# Hàm main để chạy ứng dụng
if __name__ == '__main__':
    app.run(debug = True)
    