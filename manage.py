import os
from flask_script import Manager, Server
from cli import CreateEnvironment, GunicornServer
from srv import create_app

app = create_app()

manager = Manager(app)

manager.add_command('setenv', CreateEnvironment())

manager.add_command('server', Server(host=os.getenv('APP_HOST', 'localhost'),
                                     port=int(os.getenv('APP_PORT', 5000))))

manager.add_command("production", GunicornServer())

if __name__ == '__main__':
    manager.run()
