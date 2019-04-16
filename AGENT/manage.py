import os
from flask_script import Manager, Server
from app import app

manager = Manager(app)

manager.add_command('server', Server(host=os.getenv('APP_HOST', 'localhost'),
                                     port=int(os.getenv('APP_PORT', 5000))))


if __name__ == '__main__':
    manager.run()
