from django.shortcuts import render
from django.http import HttpResponse

def dashboard_home(request):
    return HttpResponse("""
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>منصة المسابقات الرياضية</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #4CAF50; }
            .links { margin: 30px 0; }
            .links a { 
                display: inline-block; 
                margin: 10px; 
                padding: 15px 30px; 
                background: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 5px; 
            }
        </style>
    </head>
    <body>
        <h1>🎓 منصة المسابقات الرياضية</h1>
        <p>مرحباً بكم في منصة المسابقات الرياضية التفاعلية</p>
        <div class="links">
            <a href="/admin/">لوحة الإدارة</a>
            <a href="/accounts/login/">تسجيل دخول المعلمين</a>
            <a href="/student/login/">دخول الطلاب</a>
            <a href="/competitions/">المسابقات</a>
        </div>
        <p>✅ التطبيق يعمل بنجاح!</p>
    </body>
    </html>
    """)

def student_login(request):
    return HttpResponse("""
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>دخول الطلاب</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #4CAF50; }
            .form { max-width: 400px; margin: 0 auto; }
            input { padding: 10px; margin: 10px; width: 200px; }
            button { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>👥 دخول الطلاب</h1>
        <div class="form">
            <p>أدخل رمز الدخول:</p>
            <input type="text" placeholder="رمز الدخول" />
            <br>
            <button>دخول</button>
            <p><small>الرمز الافتراضي: ben25</small></p>
        </div>
        <a href="/">العودة للرئيسية</a>
    </body>
    </html>
    """)
