import os
from app import app
from app import socketio

socketio.run(app, debug=True, port=5000)