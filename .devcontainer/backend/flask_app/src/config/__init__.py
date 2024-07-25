import os

class Config():
    '''
    sqlalchemy 관련 config
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BASE_DB_DIR = os.path.join(BASE_DIR, 'db')
    BASE_DB_NAME = "sqlite.db"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DB_DIR, BASE_DB_NAME))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    from .development import DEVELOPMENT_SECRET_KEY
    from .production import PRODUCTION_SECRET_KEY
    SECRET_KEYS = {
        'DEVELOPMENT_SECRET_KEY': DEVELOPMENT_SECRET_KEY,
        'PRODUCTION_SECRET_KEY': PRODUCTION_SECRET_KEY
    }

    '''
    flask-admin 관련 config
    '''
    FLASK_ADMIN_SWATCH = 'darkly' # 테마 설정