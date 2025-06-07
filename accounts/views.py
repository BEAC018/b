from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("صفحة تسجيل الدخول للمعلمين")
