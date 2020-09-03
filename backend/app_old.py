#coding=utf-8  
from flask import Flask  
from flask import request,jsonify  
from flask_cors import CORS  
from flask_socketio import SocketIO,send,emit,join_room, leave_room,close_room,rooms,disconnect
import sys
import thread
from threading import Lock
# # from urllib import unquote

app = Flask(__name__)  

CORS(app,cors_allowed_origins="*")  

socketio = SocketIO(app,cors_allowed_origins='*')  

thread_test=None
thread_test2=None
thread_lock = Lock()

# @socketio.on('message')  
# def handle_message(message):  
#     print(message)  
#     # print(unquote(message))  
#     # message = unquote(message)
#     send(message,broadcast=True)  

keep = False
test_already_print_num = 0
test2_already_print_num = 0
roomList = ["test","test2"]

class Get_Immediate_Logging_File_Test():
    def __init__(self):
        self.switch = False
        self.filename = "test.txt"
    
    def work(self):
        global test_already_print_num
        this_socketio_name = "watch_"+self.filename.split(".")[0]
        print "~~~~this_socketio_name~~~~"
        print this_socketio_name
        print "~~~~test_already_print_num~~~~"
        print test_already_print_num
        print "------start while------"
        print "~~~~self.switch~~~~"
        print self.switch

        while self.switch:
            socketio.sleep(1)
            with open(self.filename, "r") as readfile:
                lines = readfile.readlines()
                # if len(lines) > 20 and test_already_print_num == 0:
                #     #last_num = 20  #首次输出最多输出20行
                #     #经nonoob指正，修改如下
                #     test_already_print_num = len(lines) - 20

                if test_already_print_num < len(lines):
                    print_lines = lines[test_already_print_num - len(lines):]
                    for i in range(len(print_lines)):
                        if len(print_lines) == 1:
                            returnnum = test_already_print_num
                        else:
                            returnnum = i
                        # print returnnum
                        socketio.emit(this_socketio_name,
                                    {'data': print_lines[i].replace('\n',''),"already_print_num":returnnum},
                                    broadcast=True)
                        # print len(lines), test_already_print_num, print_lines[i].replace('\n','')
                    test_already_print_num = len(lines)
    
    def start(self):
        print "####start#####"
        self.switch = True
        self.work()
        print "-----#start#-----"

    def stop(self):
        self.switch = False
        print "-----stop-----"
    
    def check_status(self):
        return self.switch

class Get_Immediate_Logging_File_Test2():
    def __init__(self):
        self.switch = False
        self.filename = "test2.txt"
    
    def work(self):
        global test2_already_print_num
        this_socketio_name = "watch_"+self.filename.split(".")[0]
        print "~~~~this_socketio_name~~~~"
        print this_socketio_name
        print "~~~~test2_already_print_num~~~~"
        print test2_already_print_num
        print "------start while------"
        print "~~~~self.switch~~~~"
        print self.switch

        while self.switch:
            socketio.sleep(1)
            with open(self.filename, "r") as readfile:
                lines = readfile.readlines()
                # if len(lines) > 20 and test2_already_print_num == 0:
                #     #last_num = 20  #首次输出最多输出20行
                #     #经nonoob指正，修改如下
                #     test2_already_print_num = len(lines) - 20

                if test2_already_print_num < len(lines):
                    print_lines = lines[test2_already_print_num - len(lines):]
                    for i in range(len(print_lines)):
                        if len(print_lines) == 1:
                            returnnum = test2_already_print_num
                        else:
                            returnnum = i
                        # print returnnum
                        socketio.emit(this_socketio_name,
                                    {'data': print_lines[i].replace('\n',''),"already_print_num":returnnum},
                                    broadcast=True)
                        # print len(lines), test2_already_print_num, print_lines[i].replace('\n','')
                    test2_already_print_num = len(lines)
    
    def start(self):
        print "####start#####"
        self.switch = True
        self.work()
        print "-----#start#-----"

    def stop(self):
        self.switch = False
        print "-----stop-----"
    
    def check_status(self):
        return self.switch

#socket连接，主动连接
@socketio.on('connect')
def connect():
    print "is connected"

    global thread_test
    global thread_test2
    print "====thread===="
    print thread_test
    print thread_test2
    print "=============="
    with thread_lock:
        print "====Class===="
        if thread_test is None:
            print "---------------"
            global GILF_test
            GILF_test = Get_Immediate_Logging_File_Test()
            print GILF_test
            thread_test = socketio.start_background_task(target=GILF_test.work)
            print thread_test
            print "---------------"
        if thread_test2 is None:
            print "---------------"
            global GILF_test2
            GILF_test2 = Get_Immediate_Logging_File_Test2()
            print GILF_test2
            thread_test2 = socketio.start_background_task(target=GILF_test2.work)
            print thread_test2
            print "---------------"
        print "=============="
    print "$$$$$$$$$$$$"
    emit("re_connect", {"msg": "connected"})

@socketio.on('test')
def get_test_file():
    print "get_test_file"
    join_room("test")
    global test_already_print_num
    test_already_print_num = 0
    print "#############"
    print rooms()
    print "#############"
    print GILF_test.check_status()
    if not GILF_test.check_status():
        GILF_test.start()

@socketio.on('test2')
def get_test_file():
    print "get_test2_file"
    join_room("test2")
    global test2_already_print_num
    test2_already_print_num = 0
    print "#############"
    print rooms()
    print "#############"
    print GILF_test2.check_status()
    if not GILF_test2.check_status():
        GILF_test2.start()

@socketio.on('disconnect')  
def disconnect():  
    print('Client disconnected',request.sid)
    global keep
    keep = False
    thread.start_new_thread(timer,())
    # leave_room(room)

@app.route('/', methods=['GET'])
def index():
    return 'welcome to the chatroom!'

#接收前端发送的参数，my_event是事件名称，接收指定事件名的参数
@socketio.on('my event')
def my_event(data):
    global socket_data
    socket_data=data

@socketio.on('keep')
def keep():
    global keep
    keep = True
    # print "=========keep=========="
    # print keep

def timer():
    import time
    from datetime import datetime
    from time import strftime 
    print "-------------------------------------------"
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time.sleep(10) #60秒後檢查是否還有socket connect
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print "-------------------------------------------"
    print keep
    if not keep:
        GILF_test.stop()
        GILF_test2.stop()
    
if __name__ == '__main__':
    # app = create_app()
    # app.run(host='0.0.0.0', debug=True, port=5002)
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')

#參考 https://blog.csdn.net/qq_43076825/article/details/91489558?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param
