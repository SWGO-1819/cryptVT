from flask import Blueprint, Flask, Response, request
from exception.sign_exception import SignInValidationError, UserNotFoundError
from flask_socketio import SocketIO
import route.EncrytVoice
import requests
from config.socket_config import socketio
from Crypto.Random import get_random_bytes # type: ignore
import threading
from config.executor_config import executor
from config.encryptVoice import encryptvoice
call_bp: Blueprint = Blueprint(
    import_name=__name__,
    name='call',
    url_prefix='/call'
)

nonce=get_random_bytes(8)
def config(app: Flask, _socketio: SocketIO) -> None:
    global nonce
    nonce =  get_random_bytes(8)
    app.register_blueprint(call_bp)


@socketio.on('call_start')
def callstart(data):
    #ip 리스트 가져옴
    #print("test")
    user= requests.post("http://192.168.125.201:5000/list/iplist",json=data).json()
    
    #id: str = user['id']
    ip1: str = user['ip1']
    ip2: str = user['ip2']
    user={ip1:ip2,ip2:ip1}
    encryptvoice.set_call_dict(user)
    socketio.emit('call_start',nonce)
    #test=threading.Thread(target=tran.UDPRec, args=(user,), daemon=True)
    #test.start()