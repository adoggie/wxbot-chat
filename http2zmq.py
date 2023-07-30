# coding:utf-8


import json
import time
from threading import Thread
from collections import OrderedDict
import datetime
from flask import Flask
from wsgiref.simple_server import make_server
import fire

import json
from dateutil.parser import parse
import flask
from flask import Flask, send_file
from flask import Response, request, redirect, url_for
import zmq

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

from flask import make_response
from functools import wraps, update_wrapper

MX_PUB_ADDR = "tcp://127.0.0.1:19022"
ctx = zmq.Context()

sock = None
sock = ctx.socket(zmq.PUB)
sock.connect(MX_PUB_ADDR)


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/elmessage', methods=['POST'])
@nocache
def message_get():
    print(request.data)
    sock.send_string(request.data.decode())
    return ''


def run(host='0.0.0.0', port=51007, mx_pub='tcp://127.0.0.1:19011', debug=False):
    server = make_server(host, port, app)
    print("Server Started .. [{}:{}]".format(host, port), " mx_pub:{}".format(mx_pub))
    if debug:
        app.run(host=host, port=port, debug=True)
    server.serve_forever()

"""
export FLASK_APP=el-telemeter.py
flask run 
"""
if __name__ == '__main__':
    run()
    # fire.Fire()
