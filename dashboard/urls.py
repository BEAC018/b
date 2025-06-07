from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.student_login, name='student_login'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('export/', views.export_data, name='export_data'),
    path('reports/', views.reports_view, name='reports'),
]
