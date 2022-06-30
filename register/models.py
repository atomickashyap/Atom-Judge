from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  

# Create your models here.


# Users Profiles

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    total_score = models.FloatField(default = 0)

#Problemset

class Problems(models.Model):
    pcode = models.AutoField(primary_key = True)
    pdesc=models.TextField()
    difficulty = models.CharField(max_length = 100)
    solved_status = models.CharField(max_length = 50)
    score = models.FloatField(default = 0)

    def __str__(self) :
        return self.pcode

class TestCases(models.Model):
    pcode = models. OneToOneField(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE, primary_key = True)
    inp=models.FileField(upload_to='testcases',blank=True)
    out=models.FileField(upload_to='testcases',blank=True)

    def __str__(self):
        return self.pcode

class Submissions(models.Model):
    submission_code = models.AutoField(primary_key = True)
    pcode = models.ForeignKey(Problems, verbose_name = ('problem_id'), on_delete = models.CASCADE)
    user_id = models.ForeignKey(UserProfile, verbose_name = ('user.id'), on_delete = models.CASCADE)
    timestamp = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return str(self.timestamp)
