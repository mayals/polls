from django.urls import path
from .import views

app_name = 'users'

urlpatterns = [
    path('select-role/',views.select_role_view, name='select-role'),
    path('register/<str:role>', views.user_create_view, name='user-register'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('my_profile/',views.my_profile,name='profile')
]