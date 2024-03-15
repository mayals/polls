from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model 
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import RoleSelectForm, UserRegisterForm, UserLoginForm
from .models import AdminProfile, OwnerProfile, VoterProfile



def select_role_view(request):
    form = RoleSelectForm()
    if request.method == 'GET' and "yes" in request.GET :
        form = RoleSelectForm(request.GET)
        if form.is_valid():
           role= form.cleaned_data['role']
           messages.success(request,f'You successfully choice to be ( {role} ) please fill the form to register')
           return redirect('users:user-register', role=role)        
           
        else:
            form = RoleSelectForm()
            messages.error(request,f'Please choice!')
           
    context={
        'form' : form, 
    }
    return render(request,'users/select_role.html',context=context)
    






# Create your views here.
def user_create_view(request,role=None):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('form valid')
            new_user = form.save(commit=False)
            # if request.user.is_superuser:
            #     new_user.role = "ADMIN"
            #     new_user.save()
            #     return redirect('polls:home')
            
            if role :
                    print('role='+str(role) )
                    new_user.base_role = role
                    print("new_user.role="+str(role))
                    new_user.save()
                    messages.success(request,f'Successfull register { new_user.username }! ')
                    return redirect('users:user-login')
        
        else:
            form = UserRegisterForm()
            messages.error(request, f'Wrong registration, please try again!') 
    
    context ={
        'form' : form ,
    }
    return render(request,'users/user_register.html',context)        



def user_login(request):
    if request.method == 'POST':
        form     = UserLoginForm(request.POST)
        username    = request.POST.get('username')     # must be confirm email to can login
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username,password=password) #this user is found result only if user.is_active=True
        print('user='+str(user))
        if user is not None and user.is_active == True :
            #print('user='+ str(user))
            login(request,user)
            form = UserLoginForm()
            messages.success(request,f'welcome back {user.username} you do login successfully.')
            return redirect('polls:home')
           
        else:
            messages.error(request,f'Error in username or password!')
            return redirect('users:user-login')
            
    else:
        form = UserLoginForm()          
    
    context = {
            'title': 'Login',
            'form' : form,
    }
    return render(request,'users/user_login.html', context=context)




@login_required(login_url='users:user-login')
def user_logout(request):
    logout(request)
    return redirect('polls:home')


@login_required(login_url='users:user-login')
def my_profile(request):
    
    if request.user.role  == 'ADMIN' :
        profile = AdminProfile.objects.get(user=request.user)
        
    if request.user.role  == 'OWNER' :
        profile = OwnerProfile.objects.get(user=request.user) 
        
    if request.user.role  == 'VOTER' :
        profile = VoterProfile.objects.get(user=request.user) 
       
    
    context = {
        'title': 'My Profile',
        'profile' : profile,
    }
    return render(request,'users/profile.html',context)