from flask import (
    Flask,
    send_from_directory,
    request,
    redirect,
    make_response,
    jsonify,
    blueprints,
)
from flask_socketio import SocketIO
from src.loginmngr import LoginManager
from src.repo import create_message, get_all_messages, get_messages_count, serialize_msg

mngr = LoginManager()

app = Flask(__name__)
lotcom = blueprints.Blueprint("lotcom", __name__,static_folder="front")

sio = SocketIO(app, cors_allowed_origins="*")


def gsid():
    return request.sid  # type: ignore


@lotcom.route("/")
def index():
    if not mngr.is_logged_in(request.cookies.get("sessionid")):
        return redirect("/lotcom/login")
    return send_from_directory(lotcom.static_folder, "index.html")  # type: ignore


@lotcom.route("/login")
def login_page():
    return send_from_directory(lotcom.static_folder, "login.html")  # type: ignore


# ========== API 路由 ==========
@lotcom.route("/api/login", methods=["POST"])
def api_login():
    """处理登录/自动注册"""
    username = request.form.get("username")
    password = request.form.get("password")
    studentid = request.form.get("studentid")

    if not username or not password:
        return jsonify({"error": "请输入用户名和密码"}), 400

    # 自动注册新用户
    if not mngr.user_exists(username):
        mngr.signup(username, password, studentid)

    sessionid = mngr.login(username, password)
    if sessionid:
        rp = make_response(jsonify({"success": True, "username": username}))
        rp.set_cookie("sessionid", sessionid, httponly=True, samesite="Lax")
        sio.emit("joined", {"username": username})
        return rp
    else:
        return jsonify({"error": "用户名或密码错误"}), 401


@lotcom.route("/api/me")
def get_current_user():
    """获取当前登录用户信息"""
    sessionid = request.cookies.get("sessionid")
    if not mngr.is_logged_in(sessionid):
        return jsonify({"error": "未登录"}), 401

    username = mngr.get_username(sessionid)
    return jsonify({"username": username, "studentid": mngr.get_studentid(sessionid)})


@lotcom.route("/api/logout", methods=["POST"])
def logout():
    """退出登录"""
    sessionid = request.cookies.get("sessionid")
    if sessionid:
        mngr.logout(sessionid) if hasattr(mngr, "logout") else None
    resp = jsonify({"success": True})
    resp.delete_cookie("sessionid")
    return resp


@sio.on("message")
def handle_message(data):
    usr = mngr.get_username(request.cookies.get("sessionid"))
    if not usr:
        return

    print(f"({usr}): {data}")

    sio.emit(
        "message",
        f"({usr}): {data}",
        skip_sid=gsid(),
    )
    create_message(data, usr)


@sio.on("join")
def join(data):
    print("user joined:" + data)
    sio.emit("message", data.get("username") + " has joined the chat!")


@sio.on("connect")
def connect():
    print(f"用户{mngr.get_username(request.cookies.get('sessionid'))}来了")
    print("ta的sessionid为", request.cookies.get("sessionid"))


@sio.on("disconnect")
def disconnect():
    print("disconnected")


@sio.on("getMessages")
def get_messages():
    print("get messages")
    messages = get_all_messages()
    result = {"len": len(messages), "messages": [serialize_msg(m) for m in messages]}
    print(result)
    return result


if __name__ == "__main__":
    app.run(debug=True, port=11451)
