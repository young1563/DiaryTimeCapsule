from flask_login import UserMixin
from random import randint

from api.models.base import BaseModel, db

FILE_UPLOAD_LIMIT = 2 * 1024 * 1024
# flask-login 사용하기 위해 UserMixin 상속
class User(BaseModel, UserMixin):
    __tablename__ = 'user'                                                          
    username = db.Column(db.String(150), unique=True)                               # username unique
    email = db.Column(db.String(150), unique=True)                                  # email unique
    admin_check = db.Column(db.Boolean, default=False)                              # 관리자 권한 여부

    diaries_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    # user_diaries = db.relationship('Diary', back_populates='user', cascade='delete, delete-orphan', lazy='dynamic')             
    # user_comments = db.relationship('Comment', back_populates="user", cascade='delete, delete-orphan', lazy='dynamic')   

    profile_image = db.relationship('Image', back_populates='user', cascade='delete, delete-orphan', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def make_new_name(cls, name):
        new_name = name
        while cls.is_in_model(username=new_name):
            random_number = randint(100000, 999999)
            new_name = name + str(random_number)
        return new_name

    def update_count(self):
        self.diaries_count = self.user_diaries.count()
        self.comments_count = self.user_comments.count()
    
    def have_admin_check(self):
        return self.admin_check

    def upload_files(self, files, post_id):
        '''
        파일들 객체 생성 + s3에 업로드 + 일일 할당량 업데이트
        '''

        if not files or not files[0]: return

        for file in files:
            try:
                pass
                # File.upload_to_s3(file, post_id, self.id)
            except Exception as e:
                print(str(e) + f'{file.filename} upload 실패')
    
    def __repr__(self):
        return super().__repr__() + f'{self.username}'         

    def __str__(self):
        return super().__str__() + f'{self.username}' 
    
from wtforms import BooleanField, StringField
from flask_login import current_user
from flask_wtf import FlaskForm

from api.models.base import AdminBase

class UserAdmin(AdminBase):
    # 1. 표시 할 열 설정
    column_list = ('id', 'username', 'email', 'admin_check', 'diaries_count', 'comments_count',
    )

    # 2. 폼 데이터 설정
    permisson_check = {
        'username': StringField('username'),
        'email': StringField('email'),
        'admin_check': BooleanField('admin_check', default=False),
        # 'auth_type': IntegerField('auth_type', default=0),
    }
    create_form = type('ExtendedSignUpForm', (FlaskForm,), permisson_check)
    edit_form = type('EditForm', (FlaskForm,), permisson_check)
    
    # 4. 자신 계정 삭제 불가
    def delete_model(self, model):
        if model.id == current_user.id:
            print('Cannot delete yourself')
            return
        super().delete_model(model)
