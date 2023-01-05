from django import forms
from django.utils import timezone
from .views import Question
from django.contrib.auth.models import User
from django.core import validators
import datetime
import django.contrib.admin.widgets



class DateInput(forms.DateInput):
    input_type = 'date' 
    
def no_curse(value):
    cs = ('shit', 'fuck')
    print("CHECKIIIIIIIIIIIING")
    print("value=", value)
    for c in cs:
        if c in value:
            raise forms.ValidationError("Name should not contain curses")


class NewQuestionForm(forms.ModelForm):
    CURSES = ('shit','fuck')
    question_text = forms.CharField(label='question_text', max_length=100, validators=[validators.MinLengthValidator(5)])
    pub_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], initial=timezone.now(), widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime'}))
    
    # pub_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M']
    # , initial=timezone.now()
    # , widget=django.contrib.admin.widgets.AdminSplitDateTime())

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']

    def clean(self):
        # super(NewQuestionForm, self).clean()
        question_text  = self.cleaned_data.get('question_text')
        for c in NewQuestionForm.CURSES:
            if c in question_text:
                raise forms.ValidationError("Name should not contain curses")
        return self.cleaned_data

class DeleteMessagesForm(forms.Form):
    questions = forms.ChoiceField(
        widget = forms.CheckboxSelectMultiple,
        choices= Question.objects.values_list('id','question_text')
    )


class UserForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=100, validators=[validators.MinLengthValidator(5)])
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    # pub_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M']
    # , initial=timezone.now()
    # , widget=django.contrib.admin.widgets.AdminSplitDateTime())

    class Meta:
        model = User
        fields = ['username', 'password']
