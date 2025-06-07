from django.db import models
from django.utils import timezone

class StatisticsCache(models.Model):
    """ذاكرة تخزين مؤقت للإحصائيات"""
    cache_key = models.CharField(max_length=100, unique=True, verbose_name="مفتاح التخزين")
    cache_data = models.JSONField(verbose_name="بيانات التخزين")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    expires_at = models.DateTimeField(verbose_name="تاريخ انتهاء الصلاحية")

    class Meta:
        verbose_name = "ذاكرة تخزين إحصائيات"
        verbose_name_plural = "ذاكرة تخزين الإحصائيات"

    def __str__(self):
        return self.cache_key

    def is_expired(self):
        """تحقق من انتهاء صلاحية التخزين"""
        return timezone.now() > self.expires_at
