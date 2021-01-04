from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    
    #STOCK PATHS
    path("add_stock.html", views.add_stock, name="add_stock"),
    path("delete/<stock_id>", views.delete, name="delete"),
    path("delete_stock.html", views.delete_stock, name="delete_stock"),

    #USER PATHS
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("change_password", views.change_password, name="change_password"),
]