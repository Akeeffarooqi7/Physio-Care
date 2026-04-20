import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'physio-secret-key-2024-secure'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'physio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@physiocare.com')

    # App settings
    CLINIC_NAME = "PhysioCare Clinic"
    DOCTOR_NAME = "Dr. Sarah Johnson"
    DOCTOR_SPECIALTY = "Senior Physiotherapist & Sports Rehabilitation Specialist"
    CLINIC_PHONE = "+1 (555) 234-5678"
    CLINIC_EMAIL = "care@physiocare.com"
    CLINIC_ADDRESS = "123 Healing Street, Medical District, New York, NY 10001"
    WHATSAPP_NUMBER = "15552345678"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
