from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Competition(models.Model):
    """مسابقة رياضية"""
    DIFFICULTY_CHOICES = [
        ('easy', 'سهل'),
        ('medium', 'متوسط'),
        ('hard', 'صعب'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان المسابقة")
    description = models.TextField(blank=True, null=True, verbose_name="وصف المسابقة")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="مستوى الصعوبة")
    duration_minutes = models.IntegerField(default=30, verbose_name="مدة المسابقة (دقيقة)")
    questions_count = models.IntegerField(default=10, verbose_name="عدد الأسئلة")
    is_active = models.BooleanField(default=True, verbose_name="نشطة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="منشئ المسابقة")

    class Meta:
        verbose_name = "مسابقة"
        verbose_name_plural = "مسابقات"

    def __str__(self):
        return self.title

class MathQuestion(models.Model):
    """سؤال رياضي"""
    OPERATION_CHOICES = [
        ('addition', 'جمع'),
        ('subtraction', 'طرح'),
        ('multiplication', 'ضرب'),
        ('division', 'قسمة'),
    ]

    question_text = models.CharField(max_length=200, verbose_name="نص السؤال")
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES, verbose_name="نوع العملية")
    operand1 = models.IntegerField(verbose_name="العدد الأول")
    operand2 = models.IntegerField(verbose_name="العدد الثاني")
    correct_answer = models.IntegerField(verbose_name="الإجابة الصحيحة")
    difficulty = models.CharField(max_length=10, choices=Competition.DIFFICULTY_CHOICES, default='medium', verbose_name="مستوى الصعوبة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "سؤال رياضي"
        verbose_name_plural = "أسئلة رياضية"

    def __str__(self):
        return self.question_text

class Participant(models.Model):
    """مشارك في المسابقة"""
    name = models.CharField(max_length=100, verbose_name="اسم المشارك")
    grade = models.CharField(max_length=50, verbose_name="الصف")
    group = models.CharField(max_length=50, blank=True, null=True, verbose_name="المجموعة")
    school = models.CharField(max_length=100, blank=True, null=True, verbose_name="المدرسة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    class Meta:
        verbose_name = "مشارك"
        verbose_name_plural = "مشاركون"

    def __str__(self):
        return f"{self.name} - {self.grade}"

class StudentSession(models.Model):
    """جلسة طالب"""
    student_name = models.CharField(max_length=100, verbose_name="اسم الطالب")
    grade = models.CharField(max_length=50, verbose_name="الصف")
    session_code = models.CharField(max_length=20, verbose_name="رمز الجلسة")
    difficulty = models.CharField(max_length=10, choices=Competition.DIFFICULTY_CHOICES, default='medium', verbose_name="مستوى الصعوبة")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="وقت البداية")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="وقت الانتهاء")
    is_completed = models.BooleanField(default=False, verbose_name="مكتملة")
    total_questions = models.IntegerField(default=10, verbose_name="إجمالي الأسئلة")
    correct_answers = models.IntegerField(default=0, verbose_name="الإجابات الصحيحة")
    score = models.FloatField(default=0.0, verbose_name="النتيجة")

    class Meta:
        verbose_name = "جلسة طالب"
        verbose_name_plural = "جلسات الطلاب"

    def __str__(self):
        return f"{self.student_name} - {self.session_code}"

class StudentResponse(models.Model):
    """إجابة طالب"""
    session = models.ForeignKey(StudentSession, on_delete=models.CASCADE, verbose_name="الجلسة")
    question = models.ForeignKey(MathQuestion, on_delete=models.CASCADE, verbose_name="السؤال")
    student_answer = models.IntegerField(verbose_name="إجابة الطالب")
    is_correct = models.BooleanField(verbose_name="صحيحة")
    response_time = models.FloatField(verbose_name="وقت الإجابة (ثانية)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت الإجابة")

    class Meta:
        verbose_name = "إجابة طالب"
        verbose_name_plural = "إجابات الطلاب"

    def __str__(self):
        return f"{self.session.student_name} - {self.question.question_text}"

class CompetitionResult(models.Model):
    """نتيجة مسابقة"""
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name="المشارك")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name="المسابقة")
    score = models.FloatField(verbose_name="النتيجة")
    total_questions = models.IntegerField(verbose_name="إجمالي الأسئلة")
    correct_answers = models.IntegerField(verbose_name="الإجابات الصحيحة")
    time_taken = models.FloatField(verbose_name="الوقت المستغرق (دقيقة)")
    algebra_correct = models.IntegerField(default=0, verbose_name="الجبر الصحيح")
    geometry_correct = models.IntegerField(default=0, verbose_name="الهندسة الصحيحة")
    arithmetic_correct = models.IntegerField(default=0, verbose_name="الحساب الصحيح")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت الإكمال")

    class Meta:
        verbose_name = "نتيجة مسابقة"
        verbose_name_plural = "نتائج المسابقات"

    def __str__(self):
        return f"{self.participant.name} - {self.competition.title}"

class UserResponse(models.Model):
    """إجابة مستخدم"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    question = models.ForeignKey(MathQuestion, on_delete=models.CASCADE, verbose_name="السؤال")
    answer = models.IntegerField(verbose_name="الإجابة")
    is_correct = models.BooleanField(verbose_name="صحيحة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت الإجابة")

    class Meta:
        verbose_name = "إجابة مستخدم"
        verbose_name_plural = "إجابات المستخدمين"

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"
