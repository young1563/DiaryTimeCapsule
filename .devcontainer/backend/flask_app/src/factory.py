from flask import Flask
from api.models.user import User

def create_app(config, mode):
    '''
    플라스크의 팩토리 지정함수(app 객체 생성 함수)
    app 객체를 생성할 때 전역으로 접근하지 못하게 함 
    즉, 순환 참조 방지
    '''
    app = Flask(__name__)
    app.config.from_object(config) # 환경변수 설정 코드
    app.secret_key = config.SECRET_KEYS[f'{mode}_SECRET_KEY']
    app.config['mode'] = mode.upper()

    if mode != 'TEST':
        # third-party 관련 환경 변수 셋팅
        from api.utils.third_party import ThirdParty
        ThirdParty.init_app(app)
        ThirdParty.set_domain_config()
        ThirdParty.make_auth_url_and_set()

    # db, migrate init + 테이블 생성
    from api.models import db_migrate_setup
    db_migrate_setup(app)

    # admin 페이지에 모델뷰 추가
    add_admin_view(app)

    # blueprint 등록 코드, url_prefix를 기본으로 함
    add_blueprint(app)

    from api.utils.error import Error
    Error.error_handler_setting(app)

    # jinja2 필터 등록
    app.jinja_env.filters['datetime'] = lambda x: x.strftime('%y.%m.%d %H:%M')
    app.jinja_env.filters['round'] = lambda x: round(x, 2)

    # login_manager 설정 코드
    set_login_manager(app)

    # create_user, update_all_model_instances 명령어 추가
    add_cli(app)

    # sqlalchemy 쿼리 로깅 확인용 
    # import logging
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    
    # 스케줄러 등록
    set_scheduler(app)

    return app

def add_admin_view(app):
    # admin 페이지에 모델뷰 추가
    from flask_admin import Admin
    from api.models.base import CustomAdminIndexView
    admin = Admin(app, name='MyBlog', template_mode='bootstrap3', index_view=CustomAdminIndexView())
    from api.models import get_all_admin_models
    models_list, session = get_all_admin_models()
    for (admin_model, model) in models_list:
        admin.add_view(admin_model(model, session))

def add_blueprint(app):
    pass
    # from api.views import views
    # app.register_blueprint(views, name='views')
    # from api.auth import auth
    # app.register_blueprint(auth, name='auth', url_prefix='/auth')

def set_login_manager(app):
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app) # app 연결
    login_manager.login_view = 'auth.login' # 로그인을 꼭 해야하는 페이지 접근 시 auth.login으로 리다이렉트 설정 

    # login_required 실행 전 사용자 정보 조회 메소드
    @login_manager.user_loader
    def user_loader(user_id):
        return User.get_instance_by_id(user_id)
    
def add_cli(app):
    from click import command               # 커맨드 라인 인터페이스 작성
    from flask.cli import with_appcontext   # Flask 애플리케이션 컨텍스트
    from sqlite3 import IntegrityError      # unique 제약조건 위배
    @command(name="create_user")
    @with_appcontext
    def create_user():
        username = input("Enter username : ")
        email = input("Enter email : ")
        password = input("Enter password : ")
        post_create_permission = input("Do you want post create permission? (y/n): ")
        admin_check = input("Do you want admin check? (y/n): ")

        post_create_permission = post_create_permission.lower() == "y"
        admin_check = admin_check.lower() == "y"

        try:
            admin_user = User(
                username = username,
                email = email,
                password = password,
                post_create_permission = post_create_permission,
                admin_check = admin_check
            )
            admin_user.add_instance()
            print(f"User created!\n", admin_user)
        except IntegrityError:
            # 빨간색으로 표시
            print('\033[31m' + "Error : username or email already exists.")

    # app에 등록
    app.cli.add_command(create_user)

def set_scheduler(app):
    from flask_apscheduler import APScheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    scheduler = APScheduler(scheduler=BackgroundScheduler(daemon=True, timezone='Asia/Seoul'))
    scheduler.init_app(app)
    scheduler.start()

    # 쌓인 오류 메세지 삭제
    from api.utils.email import Email
    scheduler.add_job(
        id='delete_error_email', 
        func=Email.delete_error_email,
        args=(app,), 
        trigger=CronTrigger(hour=12),
    )
