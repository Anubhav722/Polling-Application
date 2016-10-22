from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Permission


# Create your models here.

class Question(models.Model):
    user=models.ForeignKey(User, default=1)
    question_text=models.CharField(max_length=120)
    description=models.CharField(max_length=200)
    def __unicode__(self):
        return self.question_text
        
class Choice(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=120)
    vote_count=models.IntegerField(default=0)
    user_record=models.BooleanField(default=False)
    def __unicode__(self):
        return self.choice_text
    