#!/usr/bin/env python
import os
from flask_script import Manager, Server
from app import create_app

app = create_app()

manager = Manager(app)

manager.add_command('server', Server(host=os.environ.get('APP_HOST', 'localhost'),
                                     port=int(os.environ.get('APP_PORT', 5000))))

if __name__ == '__main__':
    manager.run()
