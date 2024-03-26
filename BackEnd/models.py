from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Text

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    registrationdate = db.Column(db.DateTime, server_default=func.now())
    game_query = db.Column(db.Text)

    user_filters = db.relationship('UserFilter', backref='user', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class FilterCategory(db.Model):
    __tablename__ = 'filter_categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)

    user_filters = db.relationship('UserFilter', backref='filter_category', lazy=True)

    def __init__(self, category_name):
        self.category_name = category_name

class UserFilter(db.Model):
    __tablename__ = 'user_filters'

    user_filter_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.userid'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('filter_categories.category_id'), nullable=False)
    option_value = db.Column(db.Text)

    def __init__(self, user_id, category_id, option_value=None, text_value=None, numeric_value=None, comparison_type='eq'):
        self.user_id = user_id
        self.category_id = category_id
        self.option_value = option_value
