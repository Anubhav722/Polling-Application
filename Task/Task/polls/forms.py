from django import forms
from django.contrib.auth.models import User

from polls.models import Question, Choice

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=('username', 'email', 'password')
        
        
class QuestionForm(forms.ModelForm):
    
    class Meta:
        model=Question
        fields=('question_text', 'description',)
        
class ChoiceForm(forms.ModelForm):
    
    class Meta:
        model=Choice
        fields=('choice_text',)