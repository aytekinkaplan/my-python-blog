from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Flask uygulamasını oluştur
app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

# Veritabanı ve migrasyon araçlarını başlat
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login yöneticisini başlat
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Rotaları ve modelleri içe aktar
from app import routes, models