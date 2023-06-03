# Imports #
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Configurations #
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eedbf600942368e59f9b73eefa187ba9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# circular import prevention #
from recipeapp import routes
