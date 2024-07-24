from src.api.models.base import AdminBase, BaseModel, g_db

class Image(BaseModel):
    __tablename__ = 'image'
    name = g_db.Column(g_db.String(150))
    size = g_db.Column(g_db.Float)

    user_id = g_db.Column(g_db.Integer, g_db.ForeignKey('user.id', name='fk_file_user', ondelete='CASCADE'), nullable=False)                
    user = g_db.relationship('User', back_populates='profile_image')             

    def __repr__(self):
        return super().__repr__() + f'{self.name}'         

    def __str__(self):
        return super().__str__() + f'{self.name}'

# ------------------------------------------ Admin ------------------------------------------   
class ImageAdmin(AdminBase):
    # 1. 표시 할 열 설정
    column_list = ('id', 'name', 'size', 'user')