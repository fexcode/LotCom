from flask import Flask, send_from_directory, request, redirect, make_response, jsonify
from flask_socketio import SocketIO
from src.loginmngr import LoginManager
from src.repo import create_message, get_all_messages, get_messages_count
from .app import sio, lotcom, mngr


@lotcom.route("/api/login", methods=["POST"])
def login_api():
    """API登录端点，供前端Vue调用"""
    # 支持 FormData 和 JSON 两种格式
    if request.content_type and "application/json" in request.content_type:
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")
        studentid = data.get("studentid")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        studentid = request.form.get("studentid")

    if not username or not password:
        return jsonify({"error": "Please enter username and password"}), 400

    # 自动注册
    if not mngr.user_exists(username):
        mngr.signup(username, password, studentid)

    sessionid = mngr.login(username, password)
    if sessionid:
        rp = make_response(jsonify({"success": True, "username": username}))
        rp.set_cookie("sessionid", sessionid, httponly=True, samesite="Lax")
        # 通知其他用户有人加入
        sio.emit("joined", {"username": username})
        return rp
    else:
        return jsonify({"error": "Invalid username or password"}), 401
