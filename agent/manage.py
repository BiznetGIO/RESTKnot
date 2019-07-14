#!/usr/bin/env python3

import os
from flask_script import Manager, Server
from app import app

manager = Manager(app)

manager.add_command('server', Server(host=os.environ.get('APP_HOST', 'localhost'),
                                     port=int(os.environ.get('APP_PORT', 6968))))

if __name__ == '__main__':
    manager.run()
