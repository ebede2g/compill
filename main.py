from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import os
import threading

app = Flask(__name__, template_folder='pages', static_folder='scripts')
app.secret_key = 'magic_3'
socketio = SocketIO(app)

process = None


@app.route('/', methods=['GET'])
def index():
    return render_template('mainPage_0.html')


@socketio.on('compile_code')
def handle_compile_code(data):
    global process
    code = data['code']
    filename = 'temp.cpp'

    with open(filename, 'w') as f:
        f.write(code)

    try:
        os.remove('temp.out')
    except OSError as e:
        True

    result = subprocess.run(['g++', filename, '-o', 'temp.out'], capture_output=True, text=True)
    if result.returncode != 0:
        emit('compilation_result', {'output': result.stderr})
        return

    if os.path.exists('temp.out'):
        process = subprocess.Popen(['./temp.out'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

        def stream_output():
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                socketio.emit('compilation_result', {'output': line.rstrip()})
            process.stdout.close()

            while True:
                line = process.stderr.readline()
                if not line:
                    break
                socketio.emit('compilation_result', {'output': line.rstrip()})
            process.stderr.close()

            process.wait()

        threading.Thread(target=stream_output).start()
    else:
        socketio.emit('compilation_result', {'output': 'Error: Compiled file not found.'})


@socketio.on('stop_execution')
def handle_stop_execution():
    global process
    if process:
        process.terminate()
        process = None
        socketio.emit('compilation_result', {'output': 'Execution stopped'})
        try:
            os.remove('temp.cpp')
            os.remove('temp.out')
        except OSError as e:
            socketio.emit('compilation_result', {'output': f'Error: {e.strerror}'})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=2012)
