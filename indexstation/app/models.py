from app import DB_MANAGER
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime

class User(UserMixin, DB_MANAGER.Model):
    id = DB_MANAGER.Column(DB_MANAGER.Integer, primary_key=True)
    username = DB_MANAGER.Column(DB_MANAGER.String(64), index=True, unique=True, nullable=False)
    password = DB_MANAGER.Column(DB_MANAGER.String(128),  nullable=False)
    rating = DB_MANAGER.Column(DB_MANAGER.Integer, nullable=False)
    res = DB_MANAGER.relationship('Result', backref='author', lazy='dynamic')
# При запросе параметра выше мо\жно получить все результаты пользователя из таблицы Results.
# Аналогично для параметров с таким же именем у других классов

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        return '<Пользователь {}>'.format(self.username)

class Doc(DB_MANAGER.Model):
    id = DB_MANAGER.Column(DB_MANAGER.Integer, primary_key=True)
    name = DB_MANAGER.Column(DB_MANAGER.String(64), index=True, unique=True, nullable=False)
    path = DB_MANAGER.Column(DB_MANAGER.String(128),  nullable=False)
    processed = DB_MANAGER.Column(DB_MANAGER.Boolean, nullable=False)
    res = DB_MANAGER.relationship('Result', backref='doc', lazy='dynamic')

    def __repr__(self):
        return '<Документ {}>'.format(self.name)

class Param(DB_MANAGER.Model):
    id = DB_MANAGER.Column(DB_MANAGER.Integer, primary_key=True)
    name = DB_MANAGER.Column(DB_MANAGER.String(64), index=True, unique=True, nullable=False)
    ptype = DB_MANAGER.Column(DB_MANAGER.String(16),  nullable=False)
    res = DB_MANAGER.relationship('Result', backref='param', lazy='dynamic')

    def __repr__(self):
        return '<Параметр {}>'.format(self.name)

class Result(DB_MANAGER.Model):
    id = DB_MANAGER.Column(DB_MANAGER.Integer, primary_key=True)
    user_id = DB_MANAGER.Column(DB_MANAGER.Integer, DB_MANAGER.ForeignKey('user.id'))
    doc_id = DB_MANAGER.Column(DB_MANAGER.Integer, DB_MANAGER.ForeignKey('doc.id'))
    param_id = DB_MANAGER.Column(DB_MANAGER.Integer, DB_MANAGER.ForeignKey('param.id'))
    value = DB_MANAGER.Column(DB_MANAGER.Integer)
    start_symb = DB_MANAGER.Column(DB_MANAGER.Integer, nullable=False)
    stop_symb = DB_MANAGER.Column(DB_MANAGER.Integer, nullable=False)
    timestamp = DB_MANAGER.Column(DB_MANAGER.DateTime, index=True, default=datetime.utcnow)