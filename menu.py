import itchat
from setting import Task
import re
from itchat.content import TEXT
#msg register,set task
current=8
hasDefault=False
@itchat.msg_register(TEXT)
def setTask(msg):
    global current
    global default
    global hasDefault
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
            itchat.send(msg='当前的任务是\n群聊:'+default['nickname']+'\n消息:'
                    +default['msg']+'\n定时:'+default['time'][0]+default['time'][1]+':'
                    +default['time'][2],toUserName='filehelper') 
        elif msg['Content']=='6':
            if hasDefault:
                room=itchat.search_chatrooms(name=default['nickname'])
                if len(room)==0:
                    itchat.send(msg='未找到该群聊，请确定群聊是否已保存到通讯录或群聊名称是否正确',toUserName='filehelper')
                elif len(room)==1:
                    default['target']=room[0].UserName
                    current=8
                    dstr='nickname:'+default['nickname']+'target:'+default['target']+\
                    'msg:'+default['msg']+'time:'+default['time'][0]+' '+default['time'][1]+' '+default['time'][2]
                    with open('./default','w') as f:
                        f.write(dstr)
                    task=Task(target=default['target'],msg=default['msg'],time=default['time'])
                    '''
                    if task.startTask():
                        itchat.send(msg='任务\n群聊:'+default['nickname']+'\n消息:'+default['msg']+
                            '\n定时:'+default['time'][0]+default['time'][1]+':'+default['time'][2]
                            +'\n已启动！',toUserName='filehelper')
                    else:
                        itchat.send(msg='任务\n群聊:'+default['nickname']+'\n消息:'+default['msg']+
                            '\n定时:'+default['time'][0]+default['time'][1]+':'+default['time'][2]
                            +'\n未启动',toUserName='filehelper')
                    '''
        elif msg['Content']=='00':
            current=-1
            #TODO 终止任务
            itchat.send(msg='当前任务已取消',toUserName='filehelper')
        elif msg['Content']=='666':
            #TODO 启动任务
            flag=True
            for item in default.values():
                if len(item)==0:
                    flag=False
            if flag:
                room=itchat.search_chatrooms(name=default['nickname'])
                default['target']=room[0].UserName
                dstr='nickname:'+default['nickname']+'target:'+default['target']+\
                    'msg:'+default['msg']+'time:'+default['time'][0]+' '+default['time'][1]+' '+default['time'][2]
                with open('./default','w') as f:
                    f.write(dstr)
                task=Task(target=default['target'],msg=default['msg'],time=default['time'])
                task.startTask()
                '''
                if task.startTask():
                    itchat.send(msg='任务\n群聊:'+default['nickname']+'\n消息:'+default['msg']+
                            '\n定时:'+default['time'][0]+default['time'][1]+':'+default['time'][2]
                            +'\n已启动！',toUserName='filehelper')
                else:
                    itchat.send(msg='任务\n群聊:'+default['nickname']+'\n消息:'+default['msg']+
                        '\n定时:'+default['time'][0]+default['time'][1]+':'+default['time'][2]
                        +'\n未启动',toUserName='filehelper')   
                '''                 
            else:
                itchat.send(msg='任务\n群聊:'+default['nickname']+'\n消息:'+default['msg']+
                        '\n定时:'+default['time'][0]+default['time'][1]+':'+default['time'][2]
                        +'\n未设置完成！',toUserName='filehelper')
        elif current==1 :
            #TODO 检查名称
            room=itchat.search_chatrooms(name=msg['Content'])
            if len(room)==0:
                itchat.send(msg='未找到该群聊，请确定群聊是否已保存到通讯录或群聊名称是否正确',toUserName='filehelper')
            elif len(room)==1:
                default['nickname']=room[0].NickName
                default['target']=room[0].UserName
                itchat.send(msg='群聊选择成功',toUserName='filehelper')
                current=8
            else:
                itchat.send(msg='找到多个群聊，请输入更精确的群聊名称',toUserName='filehelper')
        elif current==2:
            default['msg']=msg['Content']
            itchat.send(msg='消息设置成功',toUserName='filehelper')
            current=8
        elif current==3:
            timemsg=msg['Content']
            timeset=re.match('\s*([今明]天)\s*([0-9]*)[:：]([0-9]*)\s*',timemsg)
            if timeset is not None:
                default['time']=[timeset.group(1),timeset.group(2),timeset.group(3)]
                itchat.send(msg='时间设置成功',toUserName='filehelper')
                current=8
            else:
                itchat.send(msg='时间设置有误，请重新设置',toUserName='filehelper')

#login
itchat.auto_login(hotReload=True)
itchat.send(msg='登录成功',toUserName='filehelper')
itchat.send(msg='操作说明：\n发送1，按照提示设置消息目标\n发送2，按照提示设置消息内容\
        \n发送3，按照提示设置发送时间\n发送666确认启动定时任务\n任何时候发送0查看当前任务\
        \n发送00取消当前任务',toUserName='filehelper')
with open('./default','r',encoding='gbk') as f:
    default=f.read()
if len(default)>0:
    content=re.match('\s*nickname:(.*)target:(.*)msg:(.*)time:(.*)\s*',default)
    default={'nickname':content.group(1),'target':content.group(2),'msg':content.group(3),\
            'time':content.group(4).split(' ')}
    itchat.send(msg='您上次的任务是\n群聊:'+default['nickname']+'\n消息:'+default['msg']
            +'\n定时:'+default['time'][0]+default['time'][1]+':'+default['time'][2]
            +'\n回复6直接启动此任务',toUserName='filehelper')
    hasDefault=True
else:
    default={'target':'','msg':'','time':''}
itchat.run()
