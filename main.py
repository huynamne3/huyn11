from flask import Flask, render_template, request
from zLocket_Tool import (
    zLocket,
    step1b_sign_in,
    step2_finalize_user,
    step3_send_friend_request,
    _rand_email_,
    _rand_pw_,
    _rand_str_,
    format_proxy
)
import pprint
import random

app = Flask(__name__)

# Đọc proxy.txt và parse thành danh sách proxy_dicts
def load_proxies():
    try:
        with open("proxy.txt", "r") as f:
            proxy_lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            return [format_proxy(p) for p in proxy_lines]
    except Exception as e:
        print(f"Lỗi đọc proxy.txt: {e}")
        return []

proxies = load_proxies()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""

    if request.method == 'POST':
        url_or_username = request.form.get('username')
        custom_name = request.form.get('custom_name') or "By DangXuanGiang.Site"
        emoji = request.form.get('emoji') == 'y'

        zl = zLocket()
        zl.NAME_TOOL = custom_name
        zl.USE_EMOJI = emoji

        try:
            uid = zl._extract_uid_locket(url_or_username)
            if not uid:
                raise ValueError("Không thể lấy UID từ đường dẫn hoặc username.")

            zl.TARGET_FRIEND_UID = uid
            result += f"✅ UID từ link: <b>{uid}</b><br>"

            success_count = 0
            failure_count = 0
            logs = ""

            for i in range(10):  # gửi 10 lần liên tục
                email = _rand_email_()
                password = _rand_pw_()
                proxy = random.choice(proxies) if proxies else None

                # Tạo tài khoản
                payload = {
                    "data": {
                        "email": email,
                        "password": password,
                        "client_email_verif": True,
                        "client_token": _rand_str_(40),
                        "platform": "ios"
                    }
                }
                response = zl.excute(
                    f"{zl.API_BASE_URL}/createAccountWithEmailPassword",
                    headers=zl.headers_locket(),
                    payload=payload
                )

                if not response or response.get('result', {}).get('status') != 200:
                    failure_count += 1
                    logs += f"❌ [{i+1}] Không tạo được tài khoản.<br>"
                    continue

                id_token = step1b_sign_in(email, password, thread_id=i, proxies_dict=proxy)
                if not id_token:
                    failure_count += 1
                    logs += f"❌ [{i+1}] Đăng nhập thất bại.<br>"
                    continue

                if not step2_finalize_user(id_token, thread_id=i, proxies_dict=proxy):
                    failure_count += 1
                    logs += f"❌ [{i+1}] Không gửi profile.<br>"
                    continue

                send_result = step3_send_friend_request(id_token, thread_id=i, proxies_dict=proxy)

                if send_result is True:
                    success_count += 1
                    logs += f"✅ [{i+1}] Gửi kết bạn thành công.<br>"
                else:
                    failure_count += 1
                    msg = send_result if isinstance(send_result, str) else "Không rõ lý do"
                    logs += f"⚠️ [{i+1}] Gửi thất bại: {msg}<br>"

            result += f"<br><strong>📊 Tổng kết:</strong> {success_count} thành công, {failure_count} thất bại.<br>{logs}"

        except Exception as e:
            result = f"❌ Lỗi: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
