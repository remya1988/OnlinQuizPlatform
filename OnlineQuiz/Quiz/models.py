from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Quiz(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,default=1,on_delete=models.DO_NOTHING)
    quiz_title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def str(self):
        return self.quiz_title

class Questions(models.Model):
    question_text = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING, related_name='questions')
    title=models.CharField(max_length=200,default="Title")
    difficulty_level=models.CharField(max_length=30,default="Beginner")#Beginner Expert Intermediate Advanced
    # choices = models.JSONField(default=list)
    option1=models.CharField(max_length=100,default="opt1")
    option2 = models.CharField(max_length=100, default="opt2")
    option3 = models.CharField(max_length=100, default="opt3")
    option4 = models.CharField(max_length=100, default="opt4")
    correct_answer = models.CharField(max_length=255)
    date=models.DateTimeField(auto_now=True,null=True)

    def str(self):
        return self.question_text

class Result(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,default=1)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,default=1)
    answer=models.CharField(max_length=255,default="ans")
    date = models.DateTimeField(auto_now=True)

class UserQuizAnswer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    cnt=models.PositiveBigIntegerField(default=1)
    marks=models.PositiveBigIntegerField()
    status=models.CharField(max_length=20,default='Failed')