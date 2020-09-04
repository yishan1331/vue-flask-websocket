# coding=utf-8 
from flask import request,jsonify,send_file,render_template
from . import main
from events import get_file,inputstatus
# from .forms import LoginForm
from .. import socketio
from .. import logfileList

import time
import _thread


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/getLoggingFile', methods=['GET'])
def getLoggingFile():
    return {"file":logfileList}

@main.route('/monitorFile/<filename>', methods=['GET'])
def monitorFile(filename):
    #註冊socketio event
    socketio.on_event(filename, get_file)
    return "ok"

@main.route('/inputfile/<status>', methods=['GET'])
def inputfile(status):
    global inputstatus
    if status == "true":
        if not inputstatus:
            inputstatus = True
            _thread.start_new_thread(writefile,())
            return "ok"
        else:
            return "already start input"
    else:
        inputstatus = False
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
        time.sleep(2)

@main.route('/cleanfile', methods=['GET'])
def clearfile():
    open('file/test.txt', 'w').close()
    open('file/test2.txt', 'w').close()
    return "ok"