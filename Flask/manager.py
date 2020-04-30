from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from SCDA import app, db, models

#Adapted from https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

if __name__ == '__main__':
    manager.run()