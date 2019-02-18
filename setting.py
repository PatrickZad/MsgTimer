import itchat
import threading
from multiprocessing import Process
from datetime import datetime
import re
import time
class Task():
    def __init__(self,target,msg,time):
        self.target=target
        self.msg=msg
        self.time=self.setTime(time)
    def setTime(self,time):
        now=datetime.now()
        year=now.year
        month=now.month
        day=now.day
        hour=int(time[1])
        minute=int(time[2])
        alarm=datetime(year,month,day,hour,minute).timestamp()
        if time[0]=='明天':
            alarm+=86400
        return int(alarm-now.timestamp())
    def __sendMsg(self):
        itchat.send_msg(msg='定时任务已启动',toUserName='filehelper')
        time.sleep(self.time)
        for t in self.target:
            sent=itchat.send_msg(msg=self.msg,toUserName=t)
        if sent:
            itchat.send_msg(msg='定时消息发送成功',toUserName='filehelper')
        else:
            itchat.send_msg(msg='定时消息发送失败',toUserName='filehelper')
    def startTask(self):
        if self.time>0:
            #p=Process(target=self.__sendMsg())
            t=threading.Thread(target=self.__sendMsg(),name='timerThread')
            t.start()
            #p.start()
            return True
        else:
            itchat.send(msg='时间设置错误',toUserName='filehelper')
            return False
