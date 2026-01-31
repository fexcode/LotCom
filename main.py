from src.routers import app,lotcom
import sys
import eventlet
import eventlet.wsgi

app.register_blueprint(lotcom, url_prefix="/lotcom")

# 如果是windows就是debug
if sys.platform == "win32":
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
else:
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 14514)), app)
