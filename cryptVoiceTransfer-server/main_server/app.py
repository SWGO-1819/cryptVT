from flask import Flask
from flask_socketio import SocketIO
from http import HTTPStatus
from route.sign import sign_bp
from route.userlist import list_bp
from route.call import call_bp
from config.socket_config import socketio
from config.executor_config import executor
from config.encryptVoice import encryptvoice
from exception.sign_exception import SignException
import handler.http_handler
import handler.sign_handler
import threading
import os

# from handler.http_handler import not_found_handler
# from handler.sign_handler import sign_error_handler

#route.sign.config(app,socketio)
#route.userlist.config(app,socketio)
# app.register_error_handler(HTTPStatus.INTERNAL_SERVER_ERROR, not_found_handler)
# app.register_error_handler(SignException, sign_error_handler)
app = Flask(__name__)
app.secret_key = 'custom-secret-key-1234'
#socketio = SocketIO(app)
handler.http_handler.config(app)
handler.sign_handler.config(app)

app.register_blueprint(sign_bp)
app.register_blueprint(list_bp)
app.register_blueprint(call_bp)
socketio.init_app(app)
executor.init_app(app)
def start_udp_thread():
    t = threading.Thread(target=encryptvoice.UDPRec, daemon=True)
    t.start()

# flask run으로 실행될 때도 백그라운드 스레드 실행
if os.environ.get("FLASK_RUN_FROM_CLI") == "true" or __name__ == "__main__":
    start_udp_thread()
if __name__ == '__main__':
    # with app.test_request_context():
    # executor.submit(encryptvoice.UDPRec)
    test=threading.Thread(target=encryptvoice.UDPRec,daemon=True)
    test.start()
    socketio.run(app)