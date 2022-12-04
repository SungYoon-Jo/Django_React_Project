from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
# from .models import Feed, Reply, Like, Bookmark, Hash
from .models import Feed
from uuid import uuid4
import os
from config.settings import MEDIA_ROOT,SECRET_ROOT,KEY_ROOT
import hashlib
from steganocryptopy.steganography import Steganography
import sqlite3
from cryptography.fernet import Fernet

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
                
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  nickname=user.nickname,
                                  text_content=feed.text_content,
                                  encrypted_image=feed.encrypted_image))
            

        return render(request,"instar/main.html", context=dict(feeds=feed_list, user=user, userhash=user.userhash))

class UploadFeed(APIView):
        def post(self, request):
            
            email = request.session.get('email', None)
            content = request.data.get('content')
            
            user = User.objects.filter(email=email).first()
            
            file = request.FILES['file']
            
            uuid_name = uuid4().hex
            
            save_path = os.path.join(MEDIA_ROOT, uuid_name)
            
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            image = uuid_name
            
            str = content
            
            m = hashlib.sha256()
            m.update(str.encode())
            temp = m.hexdigest()
            
            f = open("./encrypt/"+temp, "w")
            f.write(temp)
            f.close()
            
            Steganography.generate_key("./key/key")
            print(user.userhash)
            
            Steganography.encrypt("./key/"+user.userhash, save_path, "./encrypt/"+temp)

            uuuid_name = uuid4().hex

            secret_path = os.path.join(MEDIA_ROOT, uuuid_name)
            
            with open(secret_path, 'wb+') as destination2:
                for chunk2 in file.chunks():
                    destination2.write(chunk2)
                    
            Feed.objects.create(image=image,
                                content=temp,
                                email=email,
                                text_content=str,
                                nickname=user.nickname,
                                encrypted_image=uuuid_name
                                )
            
            return Response(status=200)
        
class DeleteFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        print(feed_id)
        
        feed_image = request.data.get('feed_image', True)
        print(feed_image)
        
        conn = sqlite3.connect ('db.sqlite3')
        
        c = conn.cursor()
        c.execute("DELETE FROM 'content_feed' WHERE id = :id", {"id":feed_id})
        
        delete_path = os.path.join(MEDIA_ROOT, feed_image)
        os.remove(delete_path)

        conn.commit()
        c.close()
        conn.close()

        return Response(status=200)
    

class Testkeyword(APIView):
    def post(self, request):
        # email = request.session.get('email', None)
        
        # feed_id = request.data.get('feed_id', None)
        # # delete_path = os.path.join(MEDIA_ROOT, feed.image)
        # print(feed_id)
        
        
        # user = User.objects.filter(email=email).first()
        # print(user.userhash)

        # secret_path = os.path.join(KEY_ROOT, user.userhash)
        
        # key = Steganography.generate_key(secret_path)
        
        # encrypted_image = Steganography.encrypt("./key/"+user.userhash,"./media/test.png","./encrypt/encrypt")
        # print(encrypted_image)
            
        # email = request.session.get('email', None)
        
        # decrypted_text = Steganography.decrypt("./key/key", "./encrypt/secret.png")

        # print(decrypted_text)


        # Steganography.write_file("./decrypt/decrypt", decrypted_text)
        
        # str = "goodday"
            
        # m = hashlib.sha256()
        # m.update(str.encode())
        # temp = m.hexdigest()
        
        # f = open("./encrypt/encrypt", "w")
        # f.write(temp)
        # f.close()
    
        # Steganography.generate_key("./key/key")
        
        # img = "./media/test.png"
        # # print(BASE_DIR)
        # encrypted = Steganography.encrypt("./key/key",img,  "./encrypt/encrypt")

        # encrypted.save("./encrypt/secret.png")
        
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
#         return render(request, 'content/profile.html', context=dict(feed_list=feed_list, 
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
        