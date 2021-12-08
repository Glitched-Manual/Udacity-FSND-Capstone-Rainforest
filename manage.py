from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from rainforest.database.models import db
from rainforest.app import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
