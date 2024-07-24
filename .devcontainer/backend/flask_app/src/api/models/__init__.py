def db_migrate_setup(app):
    from .base import g_db, g_migrate
    g_db.init_app(app)
    g_migrate.init_app(app, g_db)
    with app.app_context():
        # g_db.Model 상속한 모든 클래스 추적해서 테이블 생성
        g_db.create_all()

from .user import User, UserAdmin
from .image import Image, ImageAdmin

def get_model(arg):
    models = {
        'user': User,
        'image': Image
    }
    return models[arg]

def get_admin_model(arg):
    models = {
        'user': UserAdmin,
        'image': ImageAdmin,
    }
    return models[arg]

def get_all_admin_models():
    from .base import g_db
    arg_list = ['user', 'image']
    return [[get_admin_model(arg), get_model(arg)] for arg in arg_list], g_db.session