from django.urls import path
from . import views

urlpatterns = [
    path('', views.competition_list, name='competition_list'),
]
