from src.routers import app,lotcom
import sys

app.register_blueprint(lotcom, url_prefix="/lotcom")

# 如果是windows就是debug
if sys.platform == "win32":
    app.run(debug=True, use_reloader=False)
else:
    app.run(debug=False, port=11451)
