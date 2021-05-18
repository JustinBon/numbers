import numpy as np

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

    result =  np.load('stijnshit\\todaysnumbers.npy',allow_pickle=True).item()
    temp_dict = {}

    for item in list(result.values()):
        if item in temp_dict:
            temp_dict[item] += 1
        else:
            temp_dict[item] = 1

    emit('send data', temp_dict, broadcast=True)