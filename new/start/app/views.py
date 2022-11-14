from django.shortcuts import render
from rest_framework.views import APIView
from .models import *

class Main(APIView):
    def get(self, request):
        lists = Memo.objects.all()
        data = {'lists' : lists}
        return render(request,"main/main.html", data)

class First(APIView):
    def get(self, request, idx):
        article = Memo.objects.get(id=idx)
        data = {'article': article}
    
        return render(request, 'title.html', data)
     
    