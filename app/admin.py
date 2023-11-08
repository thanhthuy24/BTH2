from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Categories, Product
from app import app, db

admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')

class MyProductView(ModelView):
    column_list = ['id','name','price']
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    column_editable_list = ['name','price']

class MyCategoryView(ModelView):
    column_list = ['name','products']

admin.add_view(MyCategoryView(Categories, db.session))
admin.add_view(MyProductView(Product, db.session))