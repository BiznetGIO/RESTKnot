from app import socketio, app
import os
socketio

if __name__ == '__main__':
    socketio.run(app, host=os.getenv('APP_HOST', 'localhost'),
                      port=int(os.getenv('APP_PORT', 5000)))