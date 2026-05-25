from flask import Flask
from flask_socketio import SocketIO, send, request, Response


app = Flask(__name__)
socketio = SocketIO(app,  cors_allowed_origins="*")

@app.route('/')
def hello_world():
    return "."
@app.route('/sign-in', methods=['POST'])
def sign_in():
        request.authorization
        user = request.get_json()

        if user['id'] == 'admin' and user['pw'] == '1234':
            return Response(
                '{"message": "로그인이 완료되었습니다.","token": "example-token-1234"}',
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                '{"message": "로그인 정보가 올바르지 않습니다."}',
                status=401,
                mimetype='application/json'
            )
@socketio.on('example')
def example_send(msg):
    print(msg)
    for i in range(10):
        socketio.send(str(i))
        socketio.sleep(0.5)
        
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)