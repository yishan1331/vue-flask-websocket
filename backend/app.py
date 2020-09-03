#coding=utf-8  
from flask import Flask  
from flask import request,jsonify  
from flask_cors import CORS  
from flask_socketio import SocketIO,send,emit,join_room, leave_room,close_room,rooms,disconnect
import sys
import thread
from threading import Lock
import time
# # from urllib import unquote

app = Flask(__name__)  

CORS(app,cors_allowed_origins="*")  

socketio = SocketIO(app,cors_allowed_origins='*')  

thread_lock = Lock()

# @socketio.on('message')  
# def handle_message(message):  
#     print(message)  
#     # print(unquote(message))  
#     # message = unquote(message)
#     send(message,broadcast=True)  

keep = False
inputstatus = False
logfileList = ["test","test2"]

class Get_Immediate_Logging_File():
    def __init__(self):
        self.switch = False
        self.filename = ""
    
    def work(self):
        print "~~~~self.switch~~~~"
        print self.switch
        print "~~~~filename~~~~"
        print self.filename
        if self.filename == "" or self.filename is None:
            print "**************"
            self.switch = False
        else:
            this_socketio_name = "watch_"+self.filename.split(".")[0]
            print "~~~~this_socketio_name~~~~"
            print this_socketio_name
            monitorLogging = globals()
            print "~~~~already_print_num~~~~"
            print monitorLogging["already_print_num"+self.filename]
            print "------start while------"

        while self.switch:
            socketio.sleep(1)
            with open(self.filename+".txt", "r") as readfile:
                lines = readfile.readlines()
                print len(lines)

                if monitorLogging["already_print_num"+self.filename] < len(lines):
                    print_lines = lines[monitorLogging["already_print_num"+self.filename] - len(lines):]
                    for i in range(len(print_lines)):
                        if len(print_lines) == 1:
                            returnnum = monitorLogging["already_print_num"+self.filename]
                        else:
                            returnnum = i
                        # print returnnum
                        socketio.emit(this_socketio_name,
                                    {'data': print_lines[i].replace('\n',''),"already_print_num":returnnum},
                                    broadcast=True)
                        print len(lines), monitorLogging["already_print_num"+self.filename], print_lines[i].replace('\n','')
                    monitorLogging["already_print_num"+self.filename] = len(lines)
    
    def start(self,filename):
        print "####start#####"
        self.switch = True
        self.filename = filename
        self.work()
        print "-----#work end#-----"

    def stop(self):
        self.switch = False
        print "-----stop-----"
    
    def check_status(self):
        return self.switch

#socket连接，主动连接
@socketio.on('connect')
def connect():
    print "is connected"
    print('Client connected',request.sid)
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
    print('Client disconnected',request.sid)
    global keep
    keep = False

    monitorLogging = globals()
    #檢查欲disconnect的request.sid目前在哪個房間，並將其從房間人數列表中移出
    monitorLogging["eachroom_peoplenum"][monitorLogging[request.sid]].remove(request.sid)
    #若房間人數列表再移除完此request.sid後長度為0，表示此房間目前無任何人，可以停止class read log file
    if len(monitorLogging["eachroom_peoplenum"][monitorLogging[request.sid]]) == 0:
        monitorLogging["loggingclass"]["thread_"+monitorLogging[request.sid]].stop()
    #再刪除global變數request.sid
    del monitorLogging[request.sid]

    #最後防線-檢查是否還有人
    thread.start_new_thread(timer,())

@app.route('/', methods=['GET'])
def index():
    return 'welcome to the chatroom!'

@app.route('/getLoggingFile', methods=['GET'])
def getLoggingFile():
    return {"file":logfileList}

@app.route('/monitorFile/<filename>', methods=['GET'])
def monitorFile(filename):
    #註冊socketio event
    socketio.on_event(filename, get_file)
    return "ok"

@app.route('/inputfile/<status>', methods=['GET'])
def inputfile(status):
    global inputstatus
    if status == "true":
        inputstatus = True
    else:
        inputstatus = False
    thread.start_new_thread(writefile,())
    return "ok"

def writefile():
    global inputstatus
    counter = 0 
    while inputstatus:
        writefile = open("file/test.txt", 'a')
        writefile.write('test' + str(counter) + '\n')
        writefile.close()
        writefile2 = open("file/test2.txt", 'a')
        writefile2.write('zzz' + str(counter) + '\n')
        writefile2.close()
        counter += 1
        # print  counter
        time.sleep(2)

@app.route('/cleanfile', methods=['GET'])
def clearfile():
    open('file/test.txt', 'w').close()
    open('file/test2.txt', 'w').close()
    return "ok"

def get_file(filename):
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
    # import time
    from datetime import datetime
    from time import strftime 
    print "-------------------------------------------"
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time.sleep(10) #60秒後檢查是否還有socket connect
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print "-------------------------------------------"
    print keep
    if not keep:
        monitorLogging = globals()
        for key,value in monitorLogging["filethreadlist"].items():
            monitorLogging["loggingclass"][key].stop()
    
if __name__ == '__main__':
    # app = create_app()
    # app.run(host='0.0.0.0', debug=True, port=5002)
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')

#參考 https://blog.csdn.net/qq_43076825/article/details/91489558?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param
