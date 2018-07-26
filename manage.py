from flask_migrate import Migrate, MigrateCommand
from api import create_app
import settings
from flask_script import Manager
from api.models import db

app = create_app(config_name=settings.APP_SETTINGS)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
