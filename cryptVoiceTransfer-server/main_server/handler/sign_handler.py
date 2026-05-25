from flask import Flask, Response

from http import HTTPStatus
from json import dumps

from exception.sign_exception import SignException

def config(app: Flask) -> None:
    app.register_error_handler(SignException, __sign_error_handler)

def __sign_error_handler(exception: SignException):
    message = {
        'message': str(exception)
    }
    response = dumps(message, ensure_ascii=False)

    return Response(
        content_type='application/json',
        response=response,
        status=HTTPStatus.BAD_REQUEST
    )

