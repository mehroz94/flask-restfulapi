# local imports
from api import create_app
import settings

config_name = settings.APP_SETTINGS
app = create_app(config_name)

if __name__ == '__main__':
    app.run()