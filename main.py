from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit


app = Flask(__name__, template_folder='pages', static_folder='scripts')
app.secret_key = 'magic_3'
socketio = SocketIO(app)





if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=2001)

