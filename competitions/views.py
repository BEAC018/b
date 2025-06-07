from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
import random
import json
from .models import (
    Competition, MathQuestion, Participant, StudentSession, 
    StudentResponse, CompetitionResult, UserResponse
)

def home(request):
    """الصفحة الرئيسية"""
    return render(request, 'competitions/home.html')

def student_login(request):
    """صفحة دخول الطلاب"""
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        grade = request.POST.get('grade', '').strip()
        access_code = request.POST.get('access_code', '').strip()
        
        # التحقق من رمز الدخول
        if access_code != getattr(settings, 'STUDENT_ACCESS_CODE', 'ben25'):
            messages.error(request, 'رمز الدخول غير صحيح')
            return render(request, 'competitions/student_login.html')
        
        if not student_name or not grade:
            messages.error(request, 'يرجى إدخال جميع البيانات المطلوبة')
            return render(request, 'competitions/student_login.html')
        
        # إنشاء جلسة جديدة
        session_code = f"S{random.randint(1000, 9999)}"
        session = StudentSession.objects.create(
            student_name=student_name,
            grade=grade,
            session_code=session_code,
            difficulty='medium'
        )
        
        # حفظ معرف الجلسة في session
        request.session['student_session_id'] = session.id
        
        return redirect('competition_start')
    
    return render(request, 'competitions/student_login.html')

def competition_start(request):
    """بداية المسابقة"""
    session_id = request.session.get('student_session_id')
    if not session_id:
        return redirect('student_login')
    
    try:
        session = StudentSession.objects.get(id=session_id)
    except StudentSession.DoesNotExist:
        return redirect('student_login')
    
    if session.is_completed:
        return redirect('competition_results')
    
    # إنشاء أسئلة عشوائية
    questions = generate_random_questions(session.difficulty, session.total_questions)
    
    context = {
        'session': session,
        'questions': questions,
        'total_questions': len(questions)
    }
    
    return render(request, 'competitions/competition.html', context)

def submit_answer(request):
    """إرسال إجابة"""
    if request.method != 'POST':
        return JsonResponse({'error': 'طريقة غير مسموحة'}, status=405)
    
    session_id = request.session.get('student_session_id')
    if not session_id:
        return JsonResponse({'error': 'جلسة غير صالحة'}, status=400)
    
    try:
        session = StudentSession.objects.get(id=session_id)
        data = json.loads(request.body)
        
        question_id = data.get('question_id')
        student_answer = data.get('answer')
        response_time = data.get('response_time', 0)
        
        question = get_object_or_404(MathQuestion, id=question_id)
        is_correct = int(student_answer) == question.correct_answer
        
        # حفظ الإجابة
        StudentResponse.objects.create(
            session=session,
            question=question,
            student_answer=student_answer,
            is_correct=is_correct,
            response_time=response_time
        )
        
        # تحديث النتيجة
        if is_correct:
            session.correct_answers += 1
            session.save()
        
        return JsonResponse({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': question.correct_answer
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def complete_competition(request):
    """إكمال المسابقة"""
    session_id = request.session.get('student_session_id')
    if not session_id:
        return redirect('student_login')
    
    try:
        session = StudentSession.objects.get(id=session_id)
        session.is_completed = True
        session.end_time = timezone.now()
        session.score = (session.correct_answers / session.total_questions) * 100
        session.save()
        
        return redirect('competition_results')
        
    except StudentSession.DoesNotExist:
        return redirect('student_login')

def competition_results(request):
    """نتائج المسابقة"""
    session_id = request.session.get('student_session_id')
    if not session_id:
        return redirect('student_login')
    
    try:
        session = StudentSession.objects.get(id=session_id)
        responses = StudentResponse.objects.filter(session=session)
        
        context = {
            'session': session,
            'responses': responses,
            'percentage': session.score
        }
        
        return render(request, 'competitions/results.html', context)
        
    except StudentSession.DoesNotExist:
        return redirect('student_login')

def generate_random_questions(difficulty='medium', count=10):
    """إنشاء أسئلة عشوائية"""
    questions = []
    operations = ['addition', 'subtraction', 'multiplication', 'division']
    
    for i in range(count):
        operation = random.choice(operations)
        
        if difficulty == 'easy':
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
        elif difficulty == 'medium':
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
        else:  # hard
            num1 = random.randint(50, 500)
            num2 = random.randint(50, 500)
        
        # تعديل الأرقام حسب العملية
        if operation == 'division':
            # للقسمة، نتأكد من أن النتيجة عدد صحيح
            num1 = num2 * random.randint(2, 10)
        elif operation == 'subtraction':
            # للطرح، نتأكد من أن النتيجة موجبة
            if num2 > num1:
                num1, num2 = num2, num1
        
        # حساب النتيجة
        if operation == 'addition':
            answer = num1 + num2
            question_text = f"{num1} + {num2} = ?"
        elif operation == 'subtraction':
            answer = num1 - num2
            question_text = f"{num1} - {num2} = ?"
        elif operation == 'multiplication':
            answer = num1 * num2
            question_text = f"{num1} × {num2} = ?"
        elif operation == 'division':
            answer = num1 // num2
            question_text = f"{num1} ÷ {num2} = ?"
        
        # إنشاء أو الحصول على السؤال
        question, created = MathQuestion.objects.get_or_create(
            question_text=question_text,
            operation=operation,
            operand1=num1,
            operand2=num2,
            defaults={
                'correct_answer': answer,
                'difficulty': difficulty
            }
        )
        
        questions.append(question)
    
    return questions

@login_required
def teacher_dashboard(request):
    """لوحة تحكم المعلم"""
    sessions = StudentSession.objects.all().order_by('-start_time')[:20]
    total_students = StudentSession.objects.count()
    completed_sessions = StudentSession.objects.filter(is_completed=True).count()
    
    context = {
        'sessions': sessions,
        'total_students': total_students,
        'completed_sessions': completed_sessions,
    }
    
    return render(request, 'competitions/teacher_dashboard.html', context)

def competition_list(request):
    """قائمة المسابقات"""
    competitions = Competition.objects.filter(is_active=True)
    return render(request, 'competitions/list.html', {'competitions': competitions})
