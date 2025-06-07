from django.urls import path
from . import views

urlpatterns = [
    path('', views.competition_list, name='competition_list'),
    path('home/', views.home, name='competition_home'),
    path('student/login/', views.student_login, name='student_login'),
    path('start/', views.competition_start, name='competition_start'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('complete/', views.complete_competition, name='complete_competition'),
    path('results/', views.competition_results, name='competition_results'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
