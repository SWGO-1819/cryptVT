from flask import Blueprint, Flask, Response, request
from flask_socketio import SocketIO

from json import dumps
from uuid import uuid1

from config.socket_config import socketio


chat_bp = Blueprint(
    import_name=__name__,
    name='chat',
    url_prefix='/chat'
)

@chat_bp.route('/crete-room', methods=['POST'])
def create_room() -> Response:
    room_id = uuid1() # abcd1234
    response = {
        'message': '방 생성이 완료되었습니다.',
        'room_id': room_id
    }
    socketio.on(room_id)

    return Response(
        content_type='application/json',
        response=dumps(response)
    )

@chat_bp.route('/crete-room', methods=['POST'])
def delete_room() -> Response:
    room_id = request.args.get('room_id')

    if room_id == None:
        raise Exception()
    socketio.close_room(room_id)
    response = {
        'message': '방 삭제가 완료되었습니다.'
    }

    return Response(
        content_type='application/json',
        response=dumps(response)
    )