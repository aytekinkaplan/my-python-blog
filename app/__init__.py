import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
db = SQLAlchemy(app)

print("Static folder set to:", app.static_folder)

from app import routes, models