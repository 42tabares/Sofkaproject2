from multiprocessing.connection import answer_challenge
from subprocess import CalledProcessError
from django.db import models
from random import randint

class Player(models.Model):

    name        = models.CharField(primary_key = True, max_length=50)
    score       = models.IntegerField(default="0")
    highscore   = models.IntegerField(default="0")


class Question(models.Model):
    category    = models.CharField(max_length=50)
    difficulty  = models.SmallIntegerField(default=1)
    text        = models.CharField(max_length=300)
    points      = models.FloatField(default = 0)
    answer1     = models.CharField(max_length=50)
    answer2     = models.CharField(max_length=50)
    answer3     = models.CharField(max_length=50)
    answer4     = models.CharField(max_length=50)
    called      = models.BooleanField(default="False")

    def getrandom(self, difficulty):
        QSet = self.objects.filter(called = False, difficulty = difficulty)
        Question = QSet.objects.order_by('?').first()
        Question.called = True
        Question.save()
        return Question
        

