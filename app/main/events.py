# coding=utf-8 
from flask import request
from flask_socketio import send,emit,join_room, leave_room,close_room,rooms,disconnect
from .. import socketio,logfileList
# from .routes import clearfile
import thread
from threading import Lock

thread_lock = Lock()

keep = False
inputstatus = False

class Get_Immediate_Logging_File():
    def __init__(self):
        self.switch = False
        self.filename = ""
    
    def work(self):
        if self.filename == "" or self.filename is None:
            self.switch = False
        else:
            this_socketio_name = "watch_"+self.filename.split(".")[0]
            monitorLogging = globals()

        while self.switch:
            socketio.sleep(1)
            with open("file/"+self.filename+".txt", "r") as readfile:
                lines = readfile.readlines()

                if monitorLogging["already_print_num"+self.filename] < len(lines):
                    print_lines = lines[monitorLogging["already_print_num"+self.filename] - len(lines):]
                    for i in range(len(print_lines)):
                        if len(print_lines) == 1:
                            returnnum = monitorLogging["already_print_num"+self.filename]
                        else:
                            returnnum = i
                        socketio.emit(this_socketio_name,
                                    {'data': print_lines[i].replace('\n',''),"already_print_num":returnnum},
                                    broadcast=True)
                    monitorLogging["already_print_num"+self.filename] = len(lines)
    
    def start(self,filename):
        self.switch = True
        self.filename = filename
        self.work()

    def stop(self):
        self.switch = False
    
    def check_status(self):
        return self.switch

#socket连接，主动连接
@socketio.on('connect')
def connect():
    monitorLogging = globals()
    monitorLogging[request.sid] = None
    if not monitorLogging.get("filethreadlist"):
        monitorLogging["filethreadlist"] = {}
        monitorLogging["eachroom_peoplenum"] = {}
        for i in logfileList:
            monitorLogging["filethreadlist"]["thread_"+i] = None
            monitorLogging["already_print_num"+i] = 0
            monitorLogging["eachroom_peoplenum"][i] = []
        monitorLogging["loggingclass"] = {}
    
    with thread_lock:
        for key,value in monitorLogging["filethreadlist"].items():
            if value is None:
                monitorLogging["loggingclass"][key] = Get_Immediate_Logging_File()
                monitorLogging["filethreadlist"][key] = socketio.start_background_task(target=monitorLogging["loggingclass"][key].work)
    emit("re_connect", {"msg": "connected","sid":request.sid})

@socketio.on('disconnect')  
def disconnect():
    global keep
    keep = False

    monitorLogging = globals()
    #檢查欲disconnect的request.sid目前在哪個房間，並將其從房間人數列表中移出
    if monitorLogging[request.sid] is not None:
        monitorLogging["eachroom_peoplenum"][monitorLogging[request.sid]].remove(request.sid)
        #若房間人數列表再移除完此request.sid後長度為0，表示此房間目前無任何人，可以停止class read log file
        if len(monitorLogging["eachroom_peoplenum"][monitorLogging[request.sid]]) == 0:
            monitorLogging["loggingclass"]["thread_"+monitorLogging[request.sid]].stop()
    #再刪除global變數request.sid
    del monitorLogging[request.sid]

    #最後防線-檢查是否還有人
    thread.start_new_thread(timer,())

def get_file(filename):
    print "~~~get_file~~~~"
    print filename
    join_room(filename)

    monitorLogging = globals()
    
    #先檢查此request.sid是否有在其他room
    if monitorLogging[request.sid] is not None:
        #房間人數列表移除request.sid
        monitorLogging["eachroom_peoplenum"][monitorLogging[request.sid]].remove(request.sid)
        #若房間人數列表再移除完此request.sid後長度為0，表示此房間目前無任何人，可以停止class read log file
        if len(monitorLogging["eachroom_peoplenum"][monitorLogging[request.sid]]) == 0:
            monitorLogging["loggingclass"]["thread_"+monitorLogging[request.sid]].stop()

    #更新此次request.sid欲加入的房間名稱
    monitorLogging[request.sid] = filename

    #將request.sid新增至房間人數列表中
    if request.sid not in monitorLogging["eachroom_peoplenum"][filename]:
        monitorLogging["eachroom_peoplenum"][filename].append(request.sid)

    #將already_print_num歸0
    monitorLogging["already_print_num"+filename] = 0

    if not monitorLogging["loggingclass"]["thread_"+filename].check_status():
        monitorLogging["loggingclass"]["thread_"+filename].start(filename)

@socketio.on('keep')
def keep():
    global keep
    keep = True

def timer():
    import time
    from datetime import datetime
    from time import strftime 
    print("-------------------------------------------")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(10) #60秒後檢查是否還有socket connect
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("-------------------------------------------")
    print(keep)
    if not keep:
        monitorLogging = globals()
        for key,value in monitorLogging["filethreadlist"].items():
            monitorLogging["loggingclass"][key].stop()
        global inputstatus
        inputstatus = False
        open('file/test.txt', 'w').close()
        open('file/test2.txt', 'w').close()
