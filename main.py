from flask import Flask, render_template, Request, request, redirect, make_response
from flask_socketio import SocketIO, emit
from loginmngr import LoginManager
from sql import create_message, get_all_messages, get_messages_count

mngr = LoginManager()

# 这是一个聊天室

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")


def gsid():
    return request.sid  # type: ignore


@app.route("/")
def index():
    if mngr.is_logged_in(request.cookies.get("sessionid")):
        return render_template(
            "index.html", username=mngr.get_username(request.cookies.get("sessionid"))
        )
    else:
        return redirect("/login")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        studentid = request.form.get("studentid")
        
        if not username or not password:
            return render_template(
                "login.html", error="Please enter username and password"
            )

        if not mngr.user_exists(username):
            mngr.signup(username, password, studentid)
        
        sessionid = mngr.login(username, password)
        if sessionid:
            rp = make_response(redirect("/"))
            rp.set_cookie("sessionid", sessionid)
            sio.emit("joined", {"username": username})
            return rp
        else:
            return render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")


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
    print("ta的sessionid为",request.cookies.get("sessionid"))
    sio.emit(
        "message",
        f"[系统消息] 用户{mngr.get_username(request.cookies.get('sessionid'))}来了",
    )
    for message in get_all_messages():
        sio.emit("message", message.tostr())

    sio.emit(
        "message", f"[系统消息] 已接收{get_messages_count()}条消息", skip_sid=gsid()
    )


@sio.on("disconnect")
def disconnect():
    print("disconnected")


if __name__ == "__main__":
    app.run(debug=True, port=11451)
