from django.db import models

# Create your models here.
from django.utils import timezone

#from django.contrib.auth.models import User
#from django.conf import settings
from django.contrib.auth import get_user_model


class BoardModel(models.Model):

    STATUS_CHOICES = [(1, '未完了'), (2, '作業中'), (3, '完了')]
    #author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    #author = models.ForeignKey(User,unique=False,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    #content = models.CharField(max_length=100)
    postdate = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    #author = models.CharField(max_length=50)
    #user = models.ForeignKey(User, unique=False)
    #category = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.author
