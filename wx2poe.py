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

import PyOfficeRobot
import poe
# TOKEN='8351fb0f149e8d023c9587df71a5e816'

TOKEN='k43-q3DTTA1z4nBNtdul4w%3D%3D'


from PyOfficeRobot.core.WeChatType import WeChat
from PyOfficeRobot.lib.decorator_utils.instruction_url import instruction

wx = WeChat()
def chat_by_gpt( api_key,who='adoggie'):
    wx.GetSessionList()  # 获取会话列表
    wx.ChatWith(who)  # 打开`who`聊天窗口
    temp_msg = None
    robot = '@小澜'
    client = poe.Client(api_key, proxy='http://bzz.wallizard.com:59125')
    print("Entering ",who)
    while True:
        try:
            friend_name, receive_msg = wx.GetAllMessage[-1][0], wx.GetAllMessage[-1][1]  # 获取朋友的名字、发送的信息
            # print(">>",friend_name,receive_msg)
            # if (friend_name == who) & (receive_msg != temp_msg):
            if (receive_msg != temp_msg):
                """
                条件：
                朋友名字正确:(friend_name == who)
                不是上次的对话:(receive_msg != temp_msg)
                对方内容在自己的预设里:(receive_msg in kv.keys())
                """
                print(receive_msg)
                temp_msg = receive_msg
                if receive_msg.index(robot) != -1:
                    receive_msg = receive_msg.replace(robot,'')
                    print(receive_msg)

                    reply_msg = ''
                    for chunk in client.send_message("capybara", receive_msg):
                        print(chunk["text_new"], end="", flush=True)
                        reply_msg += chunk["text_new"]
                    print(who,reply_msg)
                    # wx.SendMsg(reply_msg,who)  # 向`who`发送消息
                    wx.GetSessionList()
                    wx.ChatWith(who)  # 打开`who`聊天窗口
                    # for i in range(10):
                    wx.SendMsg(reply_msg,who)  # 向`who`发送消息
                    # PyOfficeRobot.chat.send_message(who=who, message=receive_msg)
            time.sleep(1)
        except:
            pass


PWD = os.path.abspath(os.path.dirname(__file__))

# xsub (bind ) , xpub(bind)
def run( apikey , group='001'):
    # apikey = TOKEN
    fn = os.path.join(PWD, 'route.json')
    routes = json.loads(open(fn, 'r', encoding='utf-8').read())
    talkname = ''
    for route in routes:
        if group == route['app']:
            talkname = route['talk_name']
            break
    if not talkname:
        print("Need arg 'group'")
        return
    chat_by_gpt(apikey,talkname)


if __name__ == '__main__':
    run(TOKEN,'002')
    # test()
    # fire.Fire()
