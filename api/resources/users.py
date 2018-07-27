from flask_restful import Resource, fields, marshal_with, reqparse
from api.models import User, db, RevokedTokenModel
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from utils import isolation_level
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
parser = reqparse.RequestParser()
parser.add_argument('email', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

# Implementing Fields concept of Flask-restful
resource_fields = {
    'name': fields.String,
    'email': fields.String,
    'gender': fields.String,
}

weight_resource_fields = {
    'weight': fields.Float,
}


class UserListView(Resource):
    """ With thi API, We can get all users, user by id, delete and edit an user"""

    # Get all users.
    @isolation_level(db, 'READ UNCOMMITTED')
    @marshal_with(resource_fields, envelope='users')
    def get(self):
        # Query the database and return all users
        users_query = User.query.all()
        return users_query

    # Get an user by id.
    @marshal_with(resource_fields, envelope='user')
    def post(self):
        try:
            user_id = request.values.get('user_id')
            user_obj = User.query.get(user_id)
            return user_obj
        except Exception as e:
            resp = jsonify({"error": e})
            resp.status_code = 403
            print(resp)
            return resp

    # Update an user.
    def put(self, user_id):
        try:
            user_obj = User.query.get_or_404(user_id)
            raw_data = request.values
            if raw_data:
                for k, v in raw_data.items():
                    setattr(user_obj, k, v)
                user_obj.update()

            resp = jsonify({'message': 'User updated successfully!'})
            resp.status_code = 200
            return resp
        except Exception as e:
            resp = jsonify({"error": e})
            resp.status_code = 404
            print(resp)
            return resp

    # Delete an user.
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        try:
            user.delete()
            resp = jsonify({'message': 'User has been deleted successfully!'})
            resp.status_code = 200
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class UserSignUpView(Resource):
    """ User Sign up API"""

    def post(self):
        try:
            data = parser.parse_args()
            posted_data = request.values
            name = posted_data.get('name', None)
            email = posted_data.get('email', None)
            password = posted_data.get('password', None)
            gender = posted_data.get('gender', None)

            if User.find_by_email(email):
                resp = jsonify({'message': 'Email {} already exists'.format(data['email'])})
                resp.status_code = 403
                return resp

            user = User(name=name, email=email, password=password, gender=gender)
            user.save()
            access_token = create_access_token(identity=data['email'])
            resp = jsonify({'message': 'User created successfully!', 'user_id': user.id,
                            'access_token': access_token})
            resp.status_code = 201
            return resp
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            print(resp)
            return resp
        except SQLAlchemyError as err:
            db.session.rollback()
            resp = jsonify({"error": str(err)})
            resp.status_code = 401
            print(str(err))
            return resp


class UserWeightView(Resource):
    """ List all weights of the user """

    @marshal_with(weight_resource_fields)
    @jwt_required
    def get(self, user_id):
        try:
            weights = User.query.get(user_id).weights
            return weights
        except Exception as e:
            return {'error': e}, 404


class UserLogInAPIView(Resource):
    """Log in user.
    :return access_token
    """
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_email(data['email'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}

        if data['password'] == current_user.password:
            access_token = create_access_token(identity=data['email'])
            return {'message': 'Logged in as {}'.format(current_user.email),
                    'access_token': access_token},200
        else:
            return {'message': 'Wrong credentials'}, 404


class UserLogOutAPIView(Resource):
    """ Log out a user."""
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.save()
            return {'message': 'User has been logged out.'}
        except Exception as e:
            return {'message': 'Something went wrong',
                    'error': e}, 500
