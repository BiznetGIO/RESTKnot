from app import create_app
import os

socketio, app = create_app()

if __name__ == '__main__':
    socketio.run(app, host=os.getenv('APP_HOST', 'localhost'),
                      port=int(os.getenv('APP_PORT', 5000)))