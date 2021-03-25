from django.db import models
from uuid import uuid4
from datetime import datetime


# Create your models here.

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])

class Webboard(models.Model):
    writer = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    regDate = models.DateTimeField(auto_now_add=True)
    replycount = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'webboard'

class User(models.Model):
    username = models.CharField(max_length=256)
    userpassword = models.CharField(max_length=256)
    usermail = models.CharField(max_length=256)
    regDate = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'user'

class Boardreply(models.Model):
    boardId = models.CharField(max_length=256)
    replywriter = models.CharField(max_length=256)
    replycontent = models.TextField()
    regdate = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'boardreply'



    




