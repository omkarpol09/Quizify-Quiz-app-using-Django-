from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    eventName = models.CharField(max_length=255, unique=True, help_text='Name of the event')
    description = models.TextField(blank=True, help_text='Detailed description of the event')
    image = models.ImageField(upload_to='photos/', default='photos/default.png', help_text='Event image/poster')

    def __str__(self):
        return self.eventName
    
class QuizQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventQuiz')
    question = models.TextField(help_text='The quiz question')
    optionA = models.CharField(max_length=255, help_text='Option A')
    optionB = models.CharField(max_length=255, help_text='Option B')
    optionC = models.CharField(max_length=255, help_text='Option C')
    optionD = models.CharField(max_length=255, help_text='Option D')
    answer = models.CharField(
        max_length=1, 
        choices= [('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')],
        help_text='Correct answer option'
    )

    def __str__(self):
        return f'{self.event.eventName}: {self.question[:50]}'
    
class QuizResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE) 
    selected_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]) 
    score = models.IntegerField()
    