import json
import time ,datetime
import os
import string
import sys
import time
import traceback
from random import randint
import zmq
import fire

MX_SUB_ADDR = "tcp://127.0.0.1:19011"
MX_PUB_ADDR = "tcp://127.0.0.1:19022"

import PyOfficeRobot
"""
https://gist.github.com/minrk/4667957
"""



ctx = zmq.Context()

# https://blog.csdn.net/weixin_43214364/article/details/82811095

PWD = os.path.abspath(os.path.dirname(__file__))

# xsub (bind ) , xpub(bind)
def run(sub_addr=MX_SUB_ADDR, **kvs):
    print("connect to message server:", sub_addr)

    sub = ctx.socket(zmq.SUB)
    # sub.connect(sub_addr)
    sub.bind(MX_PUB_ADDR)
    sub.setsockopt(zmq.SUBSCRIBE, b'')

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    while True:
        events = dict(poller.poll(1000))
        if sub in events:
            try:
                msg = sub.recv_string()
                parseMessage(msg)
            except:
                traceback.print_exc()


def parseMessage(msg):
    data = json.loads(msg)
    app = data['app'] or ''
    code = data['code'] or ''
    message = data['message'] or ''

    fn = os.path.join(PWD, 'route.json')
    routes = json.loads(open(fn,'r',encoding='utf-8').read())

    for route in routes:
        if app == route['app'] and code == route['code']:
            talkname = route['talk_name']
            PyOfficeRobot.chat.send_message(who=talkname, message=message )

def test():
    fn = os.path.join(PWD, 'route.json')
    routes = json.loads(open(fn, 'r',encoding='utf-8').read())

if __name__ == '__main__':
    run()
    # test()
    # fire.Fire()
