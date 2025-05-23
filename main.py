
from flask import Flask, request, jsonify
from zLocket_Tool import run_spam  # Hàm spam cần định nghĩa sẵn trong zLocket_Tool.py

app = Flask(__name__)

@app.route('/')
def home():
    return "API zLocket Tool đang hoạt động."

@app.route('/spam', methods=['POST'])
def spam():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({"error": "Thiếu username"}), 400
    result = run_spam(username)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
