from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User


#Languages Options
Languages = (
    ('c', 'C Language'),
    ('cpp', 'C++'),
    ('py', 'Python'),
)

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    total_score = models.FloatField(default = 0)

#Problem Set
class Problems(models.Model):
    pcode = models.AutoField(primary_key = True)
    pdesc = models.CharField(max_length = 255)
    difficulty = models.CharField(max_length = 200)
    rating = models.FloatField(default = 0)

class Verdicts(models.Model):
    pcode = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE)
    user_id = models.ForeignKey(UserProfile, verbose_name = ('verdict_user_id'), on_delete = models.CASCADE)
    solved_status = models.CharField(max_length = 200)

class TestCases(models.Model):
    pcode = models.OneToOneField(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE, primary_key = True)
    imp = models.CharField(max_length = 200)
    out = models.CharField(max_length = 200)

class Submissions(models.Model):
    scode = models.AutoField(primary_key = True)
    pcode = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE)
    language = models.CharField(max_length = 10,choices=Languages)
    user_id = models.ForeignKey(UserProfile, verbose_name = ('user.id'), on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default = datetime.now, blank = True)