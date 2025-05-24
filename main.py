from flask import Flask, request, render_template
import threading
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_spam():
    target_uid = request.form['target_uid']

    def run_tool():
        os.system(f'python3 zLocket_Tool.py "{target_uid}"')

    threading.Thread(target=run_tool).start()
    return f"Đang chạy tool spam cho UID/link: {target_uid}"

if __name__ == '__main__':
    app.run(debug=True)
