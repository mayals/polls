from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser


class RoleSelectForm(forms.ModelForm):
    ROLESELECT = (
        ('OWNER', "Polls's Owner" ),
        ('VOTER', "Voter" ),
    )
    
    role = forms.CharField(label  = 'I will regist as: ',
                           widget = forms.RadioSelect(choices=ROLESELECT))

    class Meta:
            model   = CustomUser
            fields  = ['role']   
       
    


# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#a-full-example
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username","password1","password2"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self,commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
    
class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='', max_length=250, widget=forms.TextInput(attrs={'placeholder': 'username..'}))
    password = forms.CharField(label='', max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'password..'}))

    class Meta:
        model   = get_user_model()
        fields  = ("username", "password")   