"""
URL configuration for alhassan project.
إعدادات الروابط لمشروع الحسن
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_redirect(request):
    """إعادة توجيه الصفحة الرئيسية"""
    return redirect('/dashboard/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('accounts/', include('accounts.urls')),
    path('competitions/', include('competitions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('student/', include('dashboard.urls')),  # للطلاب
]

# إضافة ملفات الوسائط في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
