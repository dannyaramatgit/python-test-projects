import datetime
from django.forms import widgets, DateField
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # datpub_date = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # pub_date = DateField(initial=datetime.date.today, widget=widgets.DateInput(attrs={'type': 'date'}))
    
    def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# class User(models.Model):
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)