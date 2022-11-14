from django.db import models

class Memo(models.Model):
    memo_text = models.CharField(max_length=200)
    published_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.memo_text


