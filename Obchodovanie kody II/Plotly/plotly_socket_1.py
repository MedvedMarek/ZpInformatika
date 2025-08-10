import random
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('plotly_socket_1.html')

def background_thread():
    """Pravidelné generovanie a odosielanie dát."""
    while True:
        time.sleep(2)
        x = random.randint(0, 100)
        y = random.randint(0, 10)
        data = {"x": [x], "y": [y]}
        socketio.emit('my_data', data)

@socketio.on('connect')
def test_connect():
    print('Client connected')
    # Spustíme pozadie vlákna pre pravidelné odosielanie dát
    thread = Thread(target=background_thread)
    thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
