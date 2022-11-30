from django.db import models
from datetime import  datetime
from trips.models import Post

class Comment(models.Model):
    comment_text = models.TextField(blank=True)
    score = models.CharField(max_length=100)
    movie = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text