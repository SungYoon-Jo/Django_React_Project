from django.urls import path
from .views import UploadFeed, Main, DeleteFeed, Profile, Testkeyword
# from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark, Hashupload



urlpatterns = [
    path('main', Main.as_view()),
    path('test', Testkeyword.as_view()),
    path('upload', UploadFeed.as_view()),
     path('delete', DeleteFeed.as_view()),
     path('profile', Profile.as_view()),
    # path('reply', UploadReply.as_view()),
    # path('like', ToggleLike.as_view()),
    # path('bookmark', ToggleBookmark.as_view()),
    # path('hash', Hashupload.as_view()),
]




