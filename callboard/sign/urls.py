from django.urls import path
from .views import register_user, login_view, InvalidCode, LogoutViewCustom, code

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutViewCustom, name='logout'),
    path('signup/', register_user, name='signup'),
    path('code/', code, name='code'),
    path('code/invalid/', InvalidCode.as_view(), name='invalid_code'),
]