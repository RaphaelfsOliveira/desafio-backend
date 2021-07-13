from django.db import models
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


# Caso precise criar algum modelo para sua aplicação
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, server_default=expression.false())
    is_active = db.Column(db.Boolean, server_default=expression.true())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    id_refresh_token = db.relationship('RefreshToken', backref='User', lazy='dynamic', nullable=False)
    id_access_token = db.relationship('AccessToken', backref='User', lazy='dynamic', nullable=False)
    id_token = db.relationship('RefreshToken', backref='User', lazy='dynamic', nullable=False)
    id_scope = db.relationship('Scope', backref='User', lazy='dynamic', nullable=False)

    def __init__(self, first_name, last_name, email, is_admin=False, is_active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.is_active = is_active


class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    refresh_token = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, server_default=expression.true())
    lifetime = db.Column()

    def __init__(self, id_user):
        self.id_user = id_user


class AccessToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    access_token = db.Column(db.String(255), index=True, unique=True)
    is_active = db.Column(db.Boolean, server_default=expression.true())
    lifetime = db.Column()

    def __init__(self, id_user):
        self.id_user = id_user


class Scope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    endpoint_access = db.Column(db.String(), nullable=False) 
    create = db.Column(db.Boolean, server_default=expression.false())
    retrieve = db.Column(db.Boolean, server_default=expression.false())
    update = db.Column(db.Boolean, server_default=expression.false())
    delete = db.Column(db.Boolean, server_default=expression.false())

    def __init__(self, id_user, endpoint_access, create=False, retrieve=False, update=False, delete=False):
        self.endpoint_access = endpoint_access
        self.create = create
        self.retrieve = retrieve
        self.update = update
        self.delete = delete