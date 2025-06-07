from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """ملف شخصي للمستخدم"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    school = models.CharField(max_length=100, blank=True, null=True, verbose_name="المدرسة")
    grade = models.CharField(max_length=50, blank=True, null=True, verbose_name="الصف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "ملف شخصي"
        verbose_name_plural = "ملفات شخصية"

    def __str__(self):
        return f"ملف {self.user.username}"
