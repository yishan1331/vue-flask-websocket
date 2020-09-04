# coding=utf-8 
from flask import Flask
from flask_cors import CORS  
from flask_socketio import SocketIO
import os
socketio = SocketIO()

logfileList = ["test","test2"]

def create_app(debug=False):
    """Create an application."""
    FRONTEND_FOLDER = os.path.join(os.getcwd(),'dist')
    print FRONTEND_FOLDER

    app = Flask(__name__,template_folder=FRONTEND_FOLDER,static_folder=os.path.join(FRONTEND_FOLDER,'static'))
    CORS(app,cors_allowed_origins="*")  

    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app,cors_allowed_origins="*")
    return app

# #參考 https://blog.csdn.net/qq_43076825/article/details/91489558?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.channel_param
