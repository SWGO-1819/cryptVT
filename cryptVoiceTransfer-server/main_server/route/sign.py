from flask import Blueprint, Flask, Response, request
from json import dumps
from exception.sign_exception import SignInValidationError, UserNotFoundError
from flask_socketio import SocketIO
import requests
import json

sign_bp: Blueprint = Blueprint(
    import_name=__name__,
    name='sign',
    url_prefix='/sign'
)
socketio: SocketIO
def config(app: Flask, _socketio: SocketIO) -> None:
    global socketio
    app.register_blueprint(sign_bp)
    socketio=_socketio

@sign_bp.route('/sign-in', methods=['POST'])
def sign_in() -> Response:
    user: dict = request.get_json()
    
    if 'id' not in user:
        raise SignInValidationError(message='아이디가 입력되지 않았습니다.')
    
    if 'password' not in user:
        raise SignInValidationError(message='비밀번호가 입력되지 않았습니다.')
    data=requests.post("http://192.168.125.201:5000/sign/sign-in",json=user).json()
    if "message" in data :
        return Response(content_type='application/json',response=dumps({"result":"test"}),status=400)
    if data["id"] == user["id"]:
        return Response(content_type='application/json',response=dumps({"result":"test"}),status=200)
    return Response(content_type='application/json',response=dumps({"result":"test"}))
    # if id != 'admin' or password != '1234':
    #     raise UserNotFoundError(
    #         message='아이디 또는 비밀번호가 올바르지 않습니다.',
    #         id=id,
    #         password=password
    #     )

    


@sign_bp.route('/sign-up', methods=['POST'])
def sign_up() -> Response:
    user: dict = request.get_json()
    print(user)
    #데이터 저장 코드
    requests.post("http://192.168.125.201:5000/sign/sign-up",json=user)
    return Response(content_type='application/json')

@sign_bp.route('/check', methods=['POST'])
def check() -> Response:
    user: dict = request.get_json()
    lists=requests.post("http://192.168.125.201:5000/sign/check",json=user).json()
    if "message" in lists :
        return Response(content_type='application/json',status=400)
    if lists["id"] == user["id"]:
        return Response(content_type='application/json',status=200)
    

    return Response(content_type='application/json')