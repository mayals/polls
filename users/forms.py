from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser,CommonProfile,AdminProfile,OwnerProfile,VoterProfile


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
    password1  = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2  = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, required=True)
    email      = forms.EmailField(label="email address", required=True)
    first_name = forms.CharField(label="first name", max_length=150, required=False)
    last_name  = forms.CharField(label="last name", max_length=150, required=False)
    
    class Meta:
        model = CustomUser
        fields = ["username","password1","password2","email","first_name","last_name"]

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
    
    


class UserRegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name..'}))
    last_name  = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name..'}))
    email      = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Email..'}))
    class Meta:
        model  = CustomUser
        fields = ['email','first_name','last_name']



    
class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='', max_length=250, widget=forms.TextInput(attrs={'placeholder': 'username..'}))
    password = forms.CharField(label='', max_length=250, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'password..'}))

    class Meta:
        model   = get_user_model()
        fields  = ("username", "password")
        
        
      
      
      
      
################################## Profile ###########################333  
class CommonProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model   = CommonProfile
        fields  = ('age', 'country', 'gender')
  
  
        
class AdminProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model   = AdminProfile
        fields  = ('age', 'country', 'gender')
        
        
class OwnerProfileUpdateForm(forms.ModelForm):   
    class Meta:
        model   = OwnerProfile
        fields  = ('age', 'country', 'gender')
        
        
class VoterProfileUpdateForm(forms.ModelForm):
    class Meta:
        model   = VoterProfile
        fields  = ('age', 'country', 'gender')