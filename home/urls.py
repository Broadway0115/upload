from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('update/', views.update, name='update'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('storymap/', views.storymap, name='storymap'),
    path('checkname/<str:name>', views.checkname, name='checkname'),
    path('survey/', views.survey, name='survey'),
    path('userpattern/', views.userpattern, name='userpattern')
]
