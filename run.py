import os
from app import app
from app import socketio

socketio.run(app,port=5000)
# socketio.run(app, debug=True, port=5000)