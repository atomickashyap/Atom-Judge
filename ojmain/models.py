from http.cookiejar import DefaultCookiePolicy
from turtle import title
from django.db import models
# from ckeditor.fields import RichTextField
from datetime import datetime  
from django.contrib.auth.models import User


#Languages Options
Languages = (
    ('c', 'C Language'),
    ('cpp', 'C++'),
    ('py', 'Python'),
)

# Create your models here.

# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = RichTextField(blank = True , null = True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    total_score = models.FloatField(default = 0)
    def __str__(self) :
        return str(self.user)

#Problem Set
class Problems(models.Model):
    pcode = models.AutoField(primary_key = True)
    pname = models.CharField(max_length = 255,default='Question Name')
    pdesc = models.TextField()
    difficulty = models.CharField(max_length = 200)
    input_format  = models.TextField()
    output_format = models.TextField()
    input_TC = models.TextField()
    output_TC = models.TextField()
    rating = models.FloatField(default = 0) 
    def __str__(self) :
        return self.pname

class Verdicts(models.Model):
    pcode = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE)
    user_id = models.ForeignKey(UserProfile, verbose_name = ('verdict_user_id'), on_delete = models.CASCADE)
    solved_status = models.CharField(max_length = 200)

class TestCases(models.Model):
    pcode = models.OneToOneField(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE, primary_key = True)
    imp = models.TextField()
    out = models.TextField()
    def __str__(self) :
        return str(self.pcode)


class Submissions(models.Model):
    scode = models.AutoField(primary_key = True)
    pcode = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE)
    vrt = models.CharField(max_length = 200)
    user_id = models.ForeignKey(UserProfile, verbose_name = ('user.id'), on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default = datetime.now, blank = True)
    def __str__(self) :
        return str(self.timestamp)
