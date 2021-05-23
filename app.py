import numpy as np

from flask import Flask, session, render_template, request, flash, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

print('hello world')

@app.route("/")
def index():

    result =  np.load('stijnshit\\todaysnumbers.npy',allow_pickle=True).item()

    return render_template('index.html', data = dict_counter(result))

@app.route("/stats")
def stats():
    result =  np.load('stijnshit\\todaysnumbers.npy',allow_pickle=True).item()
    return render_template('stats.html', data = result)

@app.route("/images")
def images():
    return render_template('images.html')


@socketio.on('request data')
def get_data():
    result =  np.load('stijnshit\\todaysnumbers.npy',allow_pickle=True).item()

    emit('send data', dict_counter(result), broadcast=True)

def dict_counter(result):
    temp_dict = {}

    for item in list(result.values()):
        if item in temp_dict:
            temp_dict[item] += 1
        else:
            temp_dict[item] = 1
    return temp_dict