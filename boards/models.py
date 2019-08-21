from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField('版块名',max_length=30,unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name = '板块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,related_name='topics')
    starter = models.ForeignKey(User,related_name='topics')

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(User,related_name='posts')
    updated_by = models.ForeignKey(User,null=True,related_name='+')

