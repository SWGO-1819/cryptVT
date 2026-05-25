from flask import Blueprint, Response, request

from json import dumps

from exception.sign_exception import SignInValidationError, UserNotFoundError
from model.user_model import UserInfo
from config.database_config import database


list_bp: Blueprint = Blueprint(
    import_name=__name__,
    name='list',
    url_prefix='/list'
)

@list_bp.route('/usrlist', methods=['POST'])
def usr_list() -> Response:

    user_info = UserInfo.query.filter_by().all()
    if user_info == None:
        raise UserNotFoundError(
            message='리스트가 없습니다.'
        )
    id = [i.id for i in user_info]
    print(id)
    response = {
        'id': str(id)
    }

    return Response(
        content_type='application/json',
        response=dumps(response, ensure_ascii=False)
    )
@list_bp.route('/iplist', methods=['POST'])
def idtoip() -> Response:
    user: dict = request.get_json()
    id : str = user["id1"]
    myid : str = user["id2"]
    ip1 = UserInfo.query.filter_by(id=id).first()
    ip2 = UserInfo.query.filter_by(id=myid).first()
    response = {
        'ip1': str(ip1.ip),
        'ip2': str(ip2.ip)
    }
    print(response)
    return Response(
        content_type='application/json',
        response=dumps(response, ensure_ascii=False)
    )