# Generated by Django 5.2.1 on 2025-06-07 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cache_key', models.CharField(max_length=100, unique=True, verbose_name='مفتاح التخزين')),
                ('cache_data', models.JSONField(verbose_name='بيانات التخزين')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('expires_at', models.DateTimeField(verbose_name='تاريخ انتهاء الصلاحية')),
            ],
            options={
                'verbose_name': 'ذاكرة تخزين إحصائيات',
                'verbose_name_plural': 'ذاكرة تخزين الإحصائيات',
            },
        ),
    ]
