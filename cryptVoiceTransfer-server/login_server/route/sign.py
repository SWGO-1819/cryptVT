from flask import Blueprint, Response, request

from json import dumps

from exception.sign_exception import SignInValidationError, UserNotFoundError
from model.user_model import UserInfo
from config.database_config import database
import sqlalchemy.orm


sign_bp: Blueprint = Blueprint(
    import_name=__name__,
    name='sign',
    url_prefix='/sign'
)

@sign_bp.route('/sign-in', methods=['POST'])
def sign_in() -> Response:
    user: dict = request.get_json()

    if 'id' not in user:
        raise SignInValidationError(message='아이디가 입력되지 않았습니다.')
    
    if 'password' not in user:
        raise SignInValidationError(message='비밀번호가 입력되지 않았습니다.')

    id: str = user['id']
    password: str = user['password']
    user_info = UserInfo.query.filter_by(id = id, password=password).first()
    if user_info == None:
        raise UserNotFoundError(
            message='아이디 또는 비밀번호가 올바르지 않습니다.',
            id=id,
            password=password
        )
    
    response = {
        'id': id,
        'name': user_info.name
    }
    print(response)
    return Response(
        content_type='application/json',
        response=dumps(response, ensure_ascii=False)
    )
@sign_bp.route('/sign-up', methods=['POST'])
def sign_up() -> Response:
    user: dict = request.get_json()

    if 'id' not in user:
        raise SignInValidationError(message='아이디가 입력되지 않았습니다.')
    
    if 'password' not in user:
        raise SignInValidationError(message='비밀번호가 입력되지 않았습니다.')
    
    if 'ip' not in user:
        raise SignInValidationError(message='주소가 입력되지 않았습니다.')
    
    id: str = user['id']
    password: str = user['password']
    name: str = user['name']
    ip: str = user['ip']
    
    user=UserInfo(id=id,password=password,name=name,ip=ip)
    database.session.add(user)
    database.session.commit()
    return Response(
        content_type='application/json'
    )
@sign_bp.route('/check', methods=['POST'])
def check() -> Response:
    user: dict = request.get_json()

    if 'id' not in user:
        raise SignInValidationError(message='아이디가 입력되지 않았습니다.')
    id: str = user['id']
    user_info = UserInfo.query.filter_by(id = id).first()
    if user_info != None:
        raise UserNotFoundError(
            message='아이디가 이미 있습니다.',
            id=id
        )
    response = {
        'id': id
    }
    return Response(
        content_type='application/json',
        response=dumps(response, ensure_ascii=False)
    )