# flask-restfulapi
This is a simple User weight management REST API developed using flask-restful, JWT authentication and SQLAlchemy.

This project has been developed using MySQL database and the default database name is flask-api. You may update this in settings file.

In order to initialize the db, use following commands by going into project directory:


Python manage.py db upgrade

# Test Cases
You can run the unit tests by following command:

python tests.py 

# Endpoints
Let's say you API is running on 127.0.0.1:5000 then following will be the absolute end points:

POST 127.0.0.1:5000/login/
-- Params: [email, password]

POST 127.0.0.1:5000/logout/ -- Params: [jti] , Header: Authorization Bearer <jwt>

POST 127.0.0.1:5000/user/signup/
-- Params 
[name, Email,
Password,
Gender]

Delete 127.0.0.1:5000/user/<user_id>

Add weight POST 127.0.0.1:5000/weight/
-- Params [weight, user_id]

POST 127.0.0.1:5000/user/ -- Params  [user_id]


PUT 127.0.0.1:5000/user/ -- Params 
[user_id, name, Email,
Password,
Gender]

Show weights of user

GET 127.0.0.1:5000/user/<user_id>/weight	