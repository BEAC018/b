"""
URL configuration for alhassan project.
إعدادات الروابط لمشروع الحسن
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home_view(request):
    """الصفحة الرئيسية البسيطة"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>منصة المسابقات الرياضية</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #4CAF50; margin-bottom: 30px; }
            .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
            .btn:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 منصة المسابقات الرياضية</h1>
            <p>مرحباً بكم في منصة المسابقات الرياضية التفاعلية</p>
            <div>
                <a href="/admin/" class="btn">⚙️ لوحة الإدارة</a>
                <a href="#" class="btn" onclick="alert('قريباً: دخول الطلاب')">👥 دخول الطلاب</a>
                <a href="#" class="btn" onclick="alert('قريباً: دخول المعلمين')">👨‍🏫 دخول المعلمين</a>
                <a href="#" class="btn" onclick="alert('قريباً: المسابقات')">🏆 المسابقات</a>
            </div>
            <p style="margin-top: 30px; color: #666;">✅ التطبيق يعمل بنجاح!</p>
        </div>
    </body>
    </html>
    """)

# روابط بسيطة وآمنة
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]

# ملاحظة: التطبيقات المخصصة معطلة مؤقتاً لحل خطأ 500
# سيتم تفعيلها لاحقاً بعد إصلاح المشاكل

# إضافة ملفات الوسائط
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
