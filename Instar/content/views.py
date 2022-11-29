from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
from .models import Feed, Reply, Like, Bookmark, Hash
from uuid import uuid4
import os
from config.settings import MEDIA_ROOT
import hashlib
from steganocryptopy.steganography import Steganography
import sqlite3

class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_object_list = Feed.objects.all().order_by('-id')  # select  * from content_feed;
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content, nickname=user.nickname))
                
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  nickname=user.nickname,
                                  text_content=feed.text_content,
                                  ))
            

        
        return render(request,"instar/main.html", context=dict(feeds=feed_list, user=user))

class UploadFeed(APIView):
        def post(self, request):
            
            content = request.data.get('content')
            email = request.session.get('email', None)
            
            file = request.FILES['file']
            
            uuid_name = uuid4().hex
            
            # print("uuid : "+uuid_name)
            save_path = os.path.join(MEDIA_ROOT, uuid_name)
            # print("save_path : "+save_path)
            
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            image = uuid_name
            str = content
            
            m = hashlib.sha256()
            m.update(str.encode())
            temp = m.hexdigest()

            Feed.objects.create(image=image, content=temp, email=email, text_content=str)
            # Hash.objects.create(feed_id=feed_id, email=email, hash_content=temp)
            
            return Response(status=200)
        
class DeleteFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        
        # print(feed_id)
        conn = sqlite3.connect ('db.sqlite3')
        
        c = conn.cursor()
        c.execute("DELETE FROM 'content_feed' WHERE id = :id", {"id":feed_id})
        # c.execute("DELETE FROM 'content_feed'")
        # print(c.fetchone())       

        conn.commit()
        c.close()
        conn.close()
        
        return Response(status=200)
        
# class Hashupload(APIView):
#     def post(self, request):
        
#         feed_id = request.data.get('feed_id', None)
#         print(feed_id)
#         email = request.session.get('email', None)
        
#         content = request.data.get('content')
        
#         print(content)
        
#         str = "goodday" # 받아와야하고
        
#         m = hashlib.sha256()
#         m.update(str.encode())
#         temp = m.hexdigest()
        
#         print("temp : "+ temp)
        
#         Hash.objects.create(feed_id=feed_id, email=email, hash_content=temp)
        
#         return Response(status=200)
        
        
# class Profile(APIView): 
#     def get(self, request):
        
#         email = request.session.get('email', None)
        
#         if email is None:
#             return render(request,"user/login.html")
        
#         user = User.objects.filter(email=email).first()
        
#         if user is None:
#             return render(request,"user/login.html")
        
#         feed_list = Feed.objects.filter(email=email).all()
#         like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
#         like_feed_list = Feed.objects.filter(id__in=like_list)
#         bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
#         bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
#         return render(request, 'content/profile.html', context=dict(feed_list=feed_list, 
#                                                                     like_feed_list=like_feed_list,
#                                                                     bookmark_feed_list=bookmark_feed_list,
#                                                                     user=user, 
#                                                                     ))
    
# class UploadReply(APIView):
#     def post(self, request):
#         feed_id = request.data.get('feed_id', None)
#         reply_content = request.data.get('reply_content', None)
#         email = request.session.get('email', None)

#         Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

#         return Response(status=200)
    
# class ToggleLike(APIView):
#     def post(self, request):
#         feed_id = request.data.get('feed_id', None)
#         favorite_text = request.data.get('favorite_text', True)

#         if favorite_text == 'favorite_border':
#             is_like = True
#         else:
#             is_like = False
#         email = request.session.get('email', None)

#         like = Like.objects.filter(feed_id=feed_id, email=email).first()

#         if like:
#             like.is_like = is_like
#             like.save()
#         else:
#             Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

#         return Response(status=200)
    
# class ToggleBookmark(APIView):
#     def post(self, request):
#         feed_id = request.data.get('feed_id', None)
#         bookmark_text = request.data.get('bookmark_text', True)
#         print(bookmark_text)
#         if bookmark_text == 'bookmark_border':
#             is_marked = True
#         else:
#             is_marked = False
#         email = request.session.get('email', None)

#         bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

#         if bookmark:
#             bookmark.is_marked = is_marked
#             bookmark.save()
#         else:
#             Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

#         return Response(status=200)
        