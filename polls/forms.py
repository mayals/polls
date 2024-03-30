from django import forms
from django.core.exceptions import ValidationError
from .models import Poll,Choice
from tinymce.widgets import TinyMCE


class PollForm(forms.ModelForm):
    poll_question = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add poll headline..'}))
    
    class Meta:
            model   = Poll
            fields  = ['category','poll_question','poll_descript'] 
            widgets = {'poll_descript': TinyMCE(attrs={'placeholder' : 'Add poll description..' ,
                                                              'cols' : 80 ,
                                                              'rows' : 3,
                                                            
                                                        })} 
 
       
       
       
class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(max_length=25)

    class Meta:
            model   = Choice
            fields  = ['choice_text'] 
            
            
 
class SharePollByEmailForm(forms.Form):
        sender_name     = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name..'}))
        sender_email    = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Email..'}))
        recipient_email = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Recipient Email..'}))
        sender_comment  = forms.CharField(label='', required=True, help_text='Please add comment related to the sharing the poll', widget = forms.Textarea(attrs={'rows': 5, 'class':'form-control', 'placeholder': 'Your Comment ..'})) 
                                                                                                                                                  
        def clean_sender_name(self):
            sender_name = self.cleaned_data['sender_name']
            if len(sender_name) == 0 :
                raise forms.ValidationError('sender_name must not be empty.')
            return sender_name   
        
        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('sender_name') == "" or cleaned_data.get('sender_email') == "" or cleaned_data.get('recipient_email')  == "" :
                raise forms.ValidationError('Field not empty.')
            return cleaned_data   
       
       
    
    
