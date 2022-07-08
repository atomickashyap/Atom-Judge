from django.contrib import admin
from .models import UserProfile, Problems, TestCases, Submissions
from django.db import models



# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Problems)
admin.site.register(TestCases)
admin.site.register(Submissions)