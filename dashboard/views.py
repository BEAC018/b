from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg
from competitions.models import StudentSession, StudentResponse, MathQuestion
from accounts.models import Profile
import json

def dashboard_home(request):
    """الصفحة الرئيسية للوحة التحكم"""
    # إحصائيات عامة
    total_sessions = StudentSession.objects.count()
    completed_sessions = StudentSession.objects.filter(is_completed=True).count()
    total_questions = MathQuestion.objects.count()
    
    # أحدث الجلسات
    recent_sessions = StudentSession.objects.order_by('-start_time')[:5]
    
    context = {
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'total_questions': total_questions,
        'recent_sessions': recent_sessions,
    }
    
    return render(request, 'dashboard/home.html', context)

def student_login(request):
    """إعادة توجيه لصفحة دخول الطلاب"""
    return redirect('student_login')

@login_required
def statistics_view(request):
    """عرض الإحصائيات"""
    # إحصائيات الجلسات
    sessions_by_grade = StudentSession.objects.values('grade').annotate(
        count=Count('id'),
        avg_score=Avg('score')
    ).order_by('grade')
    
    # إحصائيات الأسئلة
    questions_by_operation = MathQuestion.objects.values('operation').annotate(
        count=Count('id')
    ).order_by('operation')
    
    # أفضل النتائج
    top_sessions = StudentSession.objects.filter(
        is_completed=True
    ).order_by('-score')[:10]
    
    context = {
        'sessions_by_grade': sessions_by_grade,
        'questions_by_operation': questions_by_operation,
        'top_sessions': top_sessions,
    }
    
    return render(request, 'dashboard/statistics.html', context)

@login_required
def export_data(request):
    """تصدير البيانات"""
    if request.method == 'POST':
        export_type = request.POST.get('export_type')
        
        if export_type == 'sessions':
            sessions = StudentSession.objects.filter(is_completed=True)
            data = []
            for session in sessions:
                data.append({
                    'student_name': session.student_name,
                    'grade': session.grade,
                    'score': session.score,
                    'correct_answers': session.correct_answers,
                    'total_questions': session.total_questions,
                    'start_time': session.start_time.isoformat(),
                    'end_time': session.end_time.isoformat() if session.end_time else None,
                })
            
            return JsonResponse({
                'success': True,
                'data': data,
                'filename': 'student_sessions.json'
            })
    
    return render(request, 'dashboard/export.html')

def reports_view(request):
    """عرض التقارير"""
    # تقرير الأداء العام
    total_students = StudentSession.objects.count()
    completed_students = StudentSession.objects.filter(is_completed=True).count()
    average_score = StudentSession.objects.filter(
        is_completed=True
    ).aggregate(avg_score=Avg('score'))['avg_score'] or 0
    
    # تقرير الصفوف
    grades_performance = StudentSession.objects.filter(
        is_completed=True
    ).values('grade').annotate(
        student_count=Count('id'),
        avg_score=Avg('score'),
        total_correct=Count('correct_answers')
    ).order_by('grade')
    
    context = {
        'total_students': total_students,
        'completed_students': completed_students,
        'average_score': round(average_score, 2),
        'grades_performance': grades_performance,
    }
    
    return render(request, 'dashboard/reports.html', context)
