from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db, models


app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)

def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(use_debugger=app.config["DEBUG"]))
manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
