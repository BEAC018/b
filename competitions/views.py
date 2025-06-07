from django.shortcuts import render
from django.http import HttpResponse

def competition_list(request):
    return HttpResponse("قائمة المسابقات الرياضية")
