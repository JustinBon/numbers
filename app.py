import os
import random

from flask import Flask, session, render_template, request, flash, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

print('hello world')

@app.route("/")
def index():
    return render_template('index.html')


@socketio.on('request data')
def get_data():
    # get your new data here and change the list to the new data
    # list should be ordered from the first item being 1 and the last item being 10

    result = [random.randint(1,20) for x in range(10)]

    emit('send data', result, broadcast=True)