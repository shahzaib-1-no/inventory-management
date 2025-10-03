from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    
    path('dashboard/add_group/',views.add_group,name='add_group'),
    path('dashboard/user_role_and_permission/',views.user_role_and_permission,name='user_role_and_permission'),
]