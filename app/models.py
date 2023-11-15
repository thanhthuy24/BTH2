# đại diện cho 1 cái database
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum

class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name

class Categories(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True,
                autoincrement=True)  # autoincrease là tự động tăng giống identity trong sql server
    name = Column(String(50), nullable=False, unique=True)
    # tạo mối quan hệ vs product => đặt product trong nháy để khi máy dịch,
    # chạy qua product bên dưới rồi mới nhận biết product bên trong relationship'product'
    products = relationship('Product', backref='category',
                            lazy=True)  # backref thêm tự động vào product 1 trường category
    # => category là đối tượng chứ không còn là id nữa

    # lazy: truy vấn lười, chờ tác động lên biến products thì mới bắt đầu truy vấn

    def __str__(self):
        return self.name

class Product(db.Model):
    id = Column(Integer, primary_key=True,
                autoincrement=True)  # autoincrease là tự động tăng giống identity trong sql server
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Categories.id), nullable=False)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='Admin', username='Admin', password=str(hashlib.md5('1234567'.encode('utf-8')).hexdigest()),user_role=UserRoleEnum.ADMIN)

        db.session.add(u)
        c1 = Categories(name='Mobile')
        c2 = Categories(name='Table')

        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        p1 = Product(name='iPhone 13', price=20000000, category_id=1,
                     image="https://th.bing.com/th/id/OIP.D2L5Emr_tkvju5Hilr22DgHaHa?pid=ImgDet&rs=1")
        p2 = Product(name='Galaxy S23', price=25000000, category_id=1,
                     image="https://th.bing.com/th/id/OIP.D2L5Emr_tkvju5Hilr22DgHaHa?pid=ImgDet&rs=1")
        p3 = Product(name='Laptop Asus', price=28000000, category_id=1,
                     image="https://th.bing.com/th/id/OIP.D2L5Emr_tkvju5Hilr22DgHaHa?pid=ImgDet&rs=1")
        p4 = Product(name='iPhone 15', price=30500000, category_id=1,
                     image="https://th.bing.com/th/id/OIP.D2L5Emr_tkvju5Hilr22DgHaHa?pid=ImgDet&rs=1")
        p5 = Product(name='iPad Pro', price=16000000, category_id=1,
                     image="https://th.bing.com/th/id/OIP.D2L5Emr_tkvju5Hilr22DgHaHa?pid=ImgDet&rs=1")

        db.session.add_all([p1, p2, p3, p4, p5])
        db.session.commit()
