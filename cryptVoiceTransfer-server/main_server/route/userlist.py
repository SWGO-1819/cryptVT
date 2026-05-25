from flask import Blueprint, Flask, Response, request
from exception.sign_exception import SignInValidationError, UserNotFoundError
from flask_socketio import SocketIO
import requests
from json import dumps
from config.socket_config import socketio
list_bp: Blueprint = Blueprint(
    import_name=__name__,
    name='list',
    url_prefix='/list'
)
def config(app: Flask, _socketio: SocketIO) -> None:
    app.register_blueprint(list_bp)

@socketio.on('usrlist')
def usrlist_socket_handler(data):
    print(data)
    # 실제 요청이 필요하면 아래 요청 사용 (서버 외부 요청으로 가정)
    try:
        user = requests.post("http://192.168.125.201:5000/list/usrlist").json()
    except Exception as e:
        print("요청 실패:", e)
        user = {"users": []}
    socketio.emit("usrlist", user)

    