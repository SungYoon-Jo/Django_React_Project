from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
# from .models import Feed, Reply, Like, Bookmark, Hash
from .models import Feed
from uuid import uuid4
import os
from config.settings import MEDIA_ROOT
import hashlib
from steganocryptopy.steganography import Steganography
import sqlite3
from cryptography.fernet import Fernet
from PIL import  Image, ImageDraw, ImageFont
import cv2

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
                                  nickname=feed.nickname,
                                  text_content=feed.text_content,
                                  encrypted_image=feed.encrypted_image,
                                  feed_hash=feed.userhash,
                                  feed_watermark_image=feed.watermark_image,
                                  ))
            

        return render(request,"instar/main.html", context=dict(feeds=feed_list,
                                                               user=user,
                                                               userhash=user.userhash,
                                                               userwatermark=user.watermark_image
                                                               ))

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
            
            hash_sha256 = hashlib.new("sha256", str.encode())
            temp = hash_sha256.hexdigest()
            
            f = open("./encrypt/"+temp, "w")
            f.write(temp)
            f.close()
            
            Steganography.generate_key("./key/key")
            
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
                                encrypted_image=uuuid_name,
                                userhash=user.userhash,
                                )
            
            return Response(status=200)
        
class DeleteFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        # print(feed_id)
        
        feed_image = request.data.get('feed_image', True)
        # print(feed_image)
        
        feed_encrypted_image = request.data.get('feed_encrypted_image', True)
        
        conn = sqlite3.connect ('db.sqlite3')
        
        c = conn.cursor()
        c.execute("DELETE FROM 'content_feed' WHERE id = :id", {"id":feed_id})
        
        delete_path = os.path.join(MEDIA_ROOT, feed_image)
        os.remove(delete_path)
        encrypted_image_path = os.path.join(MEDIA_ROOT, feed_encrypted_image)
        os.remove(encrypted_image_path)

        conn.commit()
        c.close()
        conn.close()

        return Response(status=200)
    

class Testkeyword(APIView):
    def post(self, request):
        
            # img_path = os.path.join(MEDIA_ROOT, uuuid_name)
            # image1 = Image.open(img_path)
            # width, height = image1.size
            
            # draw = ImageDraw.Draw(image1)
            # text = "Test watermark"
            
            # font = ImageFont.truetype('arial.ttf', 30)
            # textwidth, textheight = draw.textsize(text, font)
            
            # margin = 10
            # x = width - textwidth - margin
            # y = height - textheight - margin
            
            #텍스트 적용하기
            # draw.text((x, y), text, font=font)
            # image1.show()
            
            # uuuuid_name = uuid4().hex
            # watermark_image_path = os.path.join(MEDIA_ROOT, uuuuid_name)
            
            # image1.save(uuuuid_name+"png")
            
            # with open(img_path, 'wb+') as destination3:
            #     for chunk3 in file.chunks():
            #         destination3.write(chunk3)
        
        path = os.path.join(MEDIA_ROOT, "3d99b8c8118c44f29652e38f5e96a80b")
        
        image1 = Image.open(path)
        
        font = ImageFont.truetype('arial.ttf', 30)
        
        width, height = image1.size
        text = "Test watermark"
        
        textwidth, textheight = font.getsize(text)
        
        draw = ImageDraw.Draw(image1)
        
        draw.text((int(width/2)-textwidth/2, int(height/2)-int(font.size/2)), text, font=font, fill="red")

        
        # margin = 10
        # x = width - textwidth - margin
        # y = height - textheight - margin
        
        #텍스트 적용하기
        # draw.text((x, y), text, font=font)
        # image1.show()
        # save = uuid4().hex
        # save_path = os.path.join(MEDIA_ROOT, save)
        # print(path)

        # image1.save(path)

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
        