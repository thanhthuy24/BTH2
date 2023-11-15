from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import Categories, Product, UserRoleEnum
from app import app, db
from flask_login import logout_user, current_user
from flask import redirect

admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyProductView(AuthenticatedAdmin):
    column_list = ['id','name','price']
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    column_editable_list = ['name','price']

class MyCategoryView(AuthenticatedAdmin):
    column_list = ['name','products']

class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')

admin.add_view(MyCategoryView(Categories, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyStatsView(name='Thông tin báo cáo'))
