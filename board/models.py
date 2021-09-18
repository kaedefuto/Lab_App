from django.db import models

# Create your models here.
from django.utils import timezone

#from django.contrib.auth.models import User
#from django.conf import settings
from django.contrib.auth import get_user_model



class ThreadModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    postdate = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.title


class BoardModel(models.Model):

    target = models.ForeignKey(ThreadModel,blank=True, null=True,on_delete=models.CASCADE)
    human = models.CharField(max_length=100)
    content = models.TextField()
    postdate = models.DateTimeField(auto_now_add=True)
    useful_review = models.IntegerField(null=True, blank=True, default=0)
    useful_review_record = models.TextField()

    def __str__(self):
        return self.human
