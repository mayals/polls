from django import forms
from django.core.exceptions import ValidationError
from .models import Poll,Choice



class PollForm(forms.ModelForm):
    poll_question = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Qustion..'}))
    
    class Meta:
            model   = Poll
            fields  = ['poll_question']   
       
       
       
class ChoiceForm(forms.ModelForm):
    choice_text        = forms.CharField(max_length=200)

    class Meta:
            model   = Choice
            fields  = ['choice_text']   
       
       
    
    