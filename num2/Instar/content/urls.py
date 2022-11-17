from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, Two, Delete


urlpatterns = [
    path('', Profile.as_view(), name='main'),
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('two/<str:idx>', Two.as_view()),
    path('delete/<str:idx>', Delete.as_view()),
    # path('main', Main.as_view()),
]




