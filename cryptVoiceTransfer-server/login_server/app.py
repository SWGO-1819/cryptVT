from flask import Flask

from http import HTTPStatus

from route.chat import chat_bp
from route.sign import sign_bp
from route.list import list_bp

from config.database_config import database
from config.socket_config import socketio
from exception.sign_exception import SignException
from handler.http_handler import not_found_handler
from handler.sign_handler import sign_error_handler


app = Flask(__name__)
app.config['SECRET_KEY'] = 'custom-secret-key-1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/chat'
app.register_blueprint(chat_bp)
app.register_blueprint(sign_bp)
app.register_blueprint(list_bp)
app.register_error_handler(HTTPStatus.INTERNAL_SERVER_ERROR, not_found_handler)
app.register_error_handler(SignException, sign_error_handler)

database.init_app(app)
socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app,host="192.168.125.201")