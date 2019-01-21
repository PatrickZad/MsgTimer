import itchat
import setting
import re
from itchat.content import TEXT
#msg register,set task
current=8
target=False
msg=False
time=False
@itchat.msg_register(TEXT)
def setTask(msg):
    global current
    global default
    if msg['ToUserName']=='filehelper':
        if msg['Content']=='1':
            current=1
            itchat.send(msg='请回复群聊名称',toUserName='filehelper')
        elif msg['Content']=='2':
            current=2
            itchat.send(msg='请回复消息内容',toUserName='filehelper')
        elif msg['Content']=='3':
            current=3
            itchat.send(msg='请回复发送时间，格式可以为 今天hh:mm 或 明天hh:mm 两种，24小时制',toUserName='filehelper')
        elif msg['Content']=='0':
            current=0 
            itchat.send(msg='当前的任务是\n群聊:'+default['target']+'\n消息:'+default['msg']+'\n定时:'+default['time'],toUserName='filehelper') 
        elif msg['Content']=='00':
            current=-1
            #TODO 终止任务
            itchat.send(msg='当前任务已取消',toUserName='filehelper')
        elif msg['Content']=='666':
            #TODO 启动任务
            dstr='target:'+default['target']+'\nmasg:'+default['msg']+'\ntime:'+default['time']
            with open('./default','w') as f:
                f.write(dstr)
            itchat.send(msg='任务\n群聊:'+default['target']+'\n消息:'+default['msg']+'\n定时:'+default['time']+'\n已启动！',toUserName='filehelper')
        elif current==1 :
            #TODO 检查名称
            default['target']=msg['Content']
            itchat.send(msg='群聊选择成功',toUserName='filehelper')
        elif current==2:
            default['msg']=msg['Content']
            itchat.send(msg='消息设置成功',toUserName='filehelper')
        elif current==3:
            default['time']=msg['Content']
            itchat.send(msg='时间设置成功',toUserName='filehelper')


            
#login
itchat.auto_login(hotReload=True)
itchat.send(msg='登录成功',toUserName='filehelper')
with open('./default','r') as f:
    default=f.read()
if len(default)>0:
    content=re.match('\s*target:(*)\s*msg:(*)\s*time:(*)\s*',default)
    default={'target':content.group(1),'msg':content.group(2),'time':content.group(3)}
    itchat.send(msg='您上次的任务是\n群聊:'+default[target]+'\n消息:'+default['msg']+'\n定时:'+default['time']+'\n回复6直接启动此任务',toUserName='filehelper')
else:
    default={'target':' ','msg':' ','time':' '}
itchat.send(msg='操作说明：\n发送1，按照提示设置消息目标\n发送2，按照提示设置消息内容\n发送3，按照提示设置发送时间\n发送666确认启动定时任务\n任何时候发送0查看当前任务，发送00取消当前任务',toUserName='filehelper')
itchat.run()
