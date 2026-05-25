from flask import Response

from http import HTTPStatus
from json import dumps


def not_found_handler(exception):
    message = {
        'message': '요청하신 페이지/API를 찾을 수 없습니다.'
    }
    response = dumps(message, ensure_ascii=False)

    return Response(
        content_type='application/json',
        response=response,
        status=HTTPStatus.NOT_FOUND
    )