from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType, PasswordType
import jwt
import datetime
import settings
from flask import abort
db = SQLAlchemy()


class CRUD(object):
    """ Base class to perform CRUD operations."""
    def save(self):
        db.session.add(self)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()


class User(db.Model, CRUD):
    """ User model """
    _GENDERS = [
        (u'male', u'Male'),
        (u'female', u'Female')
    ]
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    gender = db.Column(ChoiceType(_GENDERS))
    weights = db.relationship('UserWeight', backref='users', lazy=True, cascade="all,delete")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, email, name, password, gender):
        self.email = email
        self.name = name
        self.password = password
        self.gender = gender

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<User: {}>".format(self.name)

    def save(self):
        if self.password and self.email:
            db.session.add(self)
            db.session.commit()
        else:
            abort(400, 'Email and Password are required.')

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e


class UserWeight(db.Model, CRUD):
    """User's weight"""
    __tablename__ = 'userweights'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, weight, user_id):
        self.weight = weight
        self.user_id = user_id

    def __str__(self):
        return self.weight

    def __repr__(self):
        return "<UserWeight: {}>".format(self.weight)


class RevokedTokenModel(db.Model, CRUD):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
