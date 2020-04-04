from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import hmrm

migrate = Migrate(hmrm.app, hmrm.db)
manager = Manager(hmrm.app)

manager.add_command('db', MigrateCommand)


if __name__ == '_main_':
    manager.run()
