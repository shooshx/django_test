from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('test', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    
    # -----
    #path('', TemplateView.as_view(template_name='user_test.html'), name='main'),
    path('', TemplateView.as_view(template_name='code_wars/page.html'), name='main'),
    path('get_user_data/', views.get_user_data, name="get_user_data"), 
    
    path('create_user/', views.create_user, name="create_user"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    
    path('add_warrior_def/', views.add_warrior_def, name="add_warrior_def"),
    path('create_team/', views.create_team, name="create_team"),
    path('join_team/', views.join_team, name="join_team")
]
