from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.appointments import appointments
    from app.routes.api import api
    from app.routes.doctor import doctor
    from app.routes.patient import patient

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(appointments, url_prefix='/appointments')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(doctor, url_prefix='/doctor')
    app.register_blueprint(patient, url_prefix='/patient')

    return app
