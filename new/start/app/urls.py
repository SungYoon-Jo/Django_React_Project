from django.urls import path
from . import views
from app.views import Main,First

urlpatterns = [
    path('main/', Main.as_view()),
    path('<str:idx>/', First.as_view()),
]