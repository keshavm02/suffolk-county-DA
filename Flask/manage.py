from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from SCDA import app, db, models

#Adapted from https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()