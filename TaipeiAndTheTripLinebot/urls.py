from django.urls import path
from . import views

app_name='TaipeiAndTheTripLinebot'
urlpatterns = [
    path('callback/', views.callback, name='callback')
]
