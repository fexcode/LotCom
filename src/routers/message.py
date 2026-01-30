from flask import Flask, render_template, request, redirect, make_response
from flask_socketio import SocketIO
from src.loginmngr import LoginManager
from src.repo import create_message, get_all_messages, get_messages_count
from .app import sio, lotcom, mngr
