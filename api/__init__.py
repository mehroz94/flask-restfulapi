from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
# local import
from instance.config import app_config
from .resources.users import UserListView, UserSignUpView, UserWeightView, UserLogInAPIView, UserLogOutAPIView
from .resources.userweigth import WeightView

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    config_name = config_name if type(config_name) == str else 'development'
    print(config_name)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    jwt = JWTManager(app)
    db.init_app(app)
    Migrate(app, db)
    api = Api(app)
    api.add_resource(UserLogInAPIView, '/login/', '/login')
    api.add_resource(UserLogOutAPIView, '/logout/', '/logout')
    api.add_resource(UserListView, '/user/', '/user/<int:user_id>')
    api.add_resource(UserSignUpView, '/user/signup/', '/user/signup/')
    api.add_resource(WeightView, '/weight/', '/userweight/')
    api.add_resource(UserWeightView, '/user/weight/', '/user/<string:user_id>/weight')
    return app