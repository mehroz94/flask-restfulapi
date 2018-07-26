from flask_restful import Resource, fields, marshal_with
from api.models import UserWeight, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

resource_fields = {
    'weight': fields.String,
    'users': fields.Nested({'email': fields.String, 'gender': fields.String})
}


class WeightView(Resource):

    @marshal_with(resource_fields, envelope='weight')
    def get(self):
        # Query the database and return all users
        users_query = UserWeight.query.all()
        return users_query

    def post(self):
        try:
            posted_data = request.values
            weight = posted_data.get('weight', None)
            user_id = posted_data.get('user_id', None)
            user_weight = UserWeight(weight=weight, user_id=user_id)
            user_weight.save()
            resp = jsonify({'message': 'Weight entered successfully!'})
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