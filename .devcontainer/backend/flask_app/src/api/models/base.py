from sqlalchemy import String, or_, func
from sqlalchemy.orm import selectinload, joinedload
from json import dumps

from api.utils.etc import Etc
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()

# relationship(관계 맺는 모델 이름, back_populates=연결 필드 이름)
# Cascade = 1:N 관계에서 1쪽에 설정
# all = 모두
# save-update = session에 변경 add 시, 연결된 모든 객체도 session에 add
# delete = 삭제될 때만
# delete-orphan = delete + 관계가 끊길 때도 추가 삭제
# lazy='selectin': 주 객체를 가져오는 쿼리에 관련된 모든 객체를 가져오는 서브쿼리를 사용하여 즉시 로드
# lazy='dynamic': 지연로딩 설정 가능 = 쿼리 객체 반환 후 사용시 쿼리 실행됨
# 실제 사용할 때는 lazy='dynamic'설정 후 sqlalchemy.orm.selectinload 메소드 사용 = N+1 문제 해결

# ForeignKey(다른 테이블의 컬럼 이름, 삭제 옵션)
# db.backref => 반대쪽 모델에서 이 모델로 역참조 들어올 때, 타고 들어올 속성 명

# User <=> Post : 1:N 관계 -> Post(N) 쪽에 relationship 설정
# Category <=> Post : 1:N 관계 -> Post(N) 쪽에 relationship 설정
# Comment <=> User, Post : N:1 관계 -> Comment(N) 쪽에 relationship 설정

class BaseModel(db.Model):
    __abstract__ = True                                                             # 추상 클래스 설정
    id = db.Column(db.Integer, primary_key=True)                                    # primary key 설정
    date_created = db.Column(db.DateTime, default=Etc.get_korea_time())

    @classmethod
    def get_query(cls, id, **kwargs):
        return db.session.get(cls, id, **kwargs)
    
    @classmethod
    def get_instance_by_id(cls, id):
        id = int(id)
        instance = cls.get_query(id)
        if not instance:
            raise Exception('No instance found with the specified id')
        else:
            return instance
    
    def to_json(self):
        return dumps(self)

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.id} '
    
    def __str__(self):
        return f'{self.__class__.__name__}: {self.id} '

from sqlalchemy.event import listens_for
@listens_for(db.session, 'before_flush')
def before_flush(session, flush_context, instances):
    for obj in session.deleted:
        if hasattr(obj, 'before_deleted_flush'):
            obj.before_deleted_flush()
    
    for obj in session.new:
        if hasattr(obj, 'before_new_flush'):
            obj.before_new_flush()

# ------------------------------------------ Admin ------------------------------------------
from flask_admin.contrib.sqla import ModelView
    
class AdminBase(ModelView):
    column_formatters = {
        'date_created': lambda view, context, model, name: model.date_created.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    def is_accessible(self):
        # if current_user.is_authenticated == True and current_user.admin_check == True:
        return True
        # else:
        #     return Error.error(403)
        
    # 사용자 지정 도구 추가
    from flask_admin.actions import action
    @action('update_model_instances', 'Update Model', 'Are you sure you want to update model for selected object?')
    def update_model_instances(self, ids):
        instances = self.model.get_all_by_ids(ids)
        for instance in instances:
            instance.fill_none_fields()
            if hasattr(instance, 'update_count'):
                instance.update_count()
        self.model.commit()