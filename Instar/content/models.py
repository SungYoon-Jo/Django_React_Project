from django.db import models

class Feed(models.Model):
    content = models.TextField()   
    text_content = models.TextField(null=True)
    image = models.TextField() 
    encrypted_image = models.TextField(null=True) 
    email = models.EmailField(default='')   
    nickname = models.CharField(max_length=24, default='')
    userhash = models.TextField(null=True, default='')
    watermark_image = models.TextField(null=True)

class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)

class Hash(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    hash_content = models.TextField()

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)
    
