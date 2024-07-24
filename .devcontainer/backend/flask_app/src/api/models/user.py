from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from werkzeug.security import generate_password_hash, check_password_hash

from src.api.models.base import AdminBase, BaseModel, g_db

# flask-login 사용하기 위해 UserMixin 상속
class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    fullname = g_db.Column(g_db.String(50))                    # 이름                                
    nickname = g_db.Column(g_db.String(50), unique=True)       # nickname unique
    login_id = g_db.Column(g_db.String(50), unique=True)       # login id unique
    password = g_db.Column(g_db.String(255))
    admin_check = g_db.Column(g_db.Boolean, default=False)      # 관리자 권한 여부  

    profile_image = g_db.relationship('Image', back_populates='user', cascade='delete, delete-orphan', lazy='dynamic')

    def __init__(self, password, **kwargs):
        self.set_password(password)
        super().__init__(**kwargs)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    @classmethod
    def user_check(cls, login_id, password):
        login_id = login_id.strip().replace(' ', '')
        user = g_db.session.query(cls).filter_by(login_id=login_id).first()
        if user:
            if not check_password_hash(password, user.password): return user
            else: return print('비밀번호가 틀렸습니다.')
        else: return print('존재하지 않는 아이디')
    
    def __repr__(self):
        return super().__repr__() + f'{self.username}'         

    def __str__(self):
        return super().__str__() + f'{self.username}' 

class UserAdmin(AdminBase):
    # 1. 표시 할 열 설정
    column_list = ('id', 'fullname', 'nickname', 'login_id', 'admin_check')

    # 2. 폼 데이터 설정
    permisson_check = {
        'fullname': StringField('fullname'),
        'nickname': StringField('nickname'),
        'id': StringField('login_id'),
        'admin_check': BooleanField('admin_check', default=False),
    }
    create_form = type('ExtendedSignUpForm', (FlaskForm,), permisson_check)
    edit_form = type('EditForm', (FlaskForm,), permisson_check)
