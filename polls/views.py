from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Poll, Choice,Category
from .forms import PollForm,ChoiceForm,SharePollByEmailForm

from .models import Choice
from django.views.generic import DetailView
from django.views.generic import ListView


def categories(request):
    categories = Category.objects.all().order_by('-polls_count')
    
    for cat in categories :
        polls = Poll.objects.all().filter(category=cat)
        polls_count = polls.count()
        cat.polls_count = polls_count
        cat.save()
        
    context={
        'title'              : 'Categories',
        'description_content': 'Categories List of polls',
        'categories'         : categories,
    }
    return render(request,'polls/categories.html',context)




def cat_detail(request,cat_slug):
    category = get_object_or_404(Category,slug=cat_slug)
    context = {
        'title': 'Category Detail',
        'description_content': 'Categories detail of polls',
        'category'  : category,
    }
    return render(request,'polls/category_detail.html',context)





class ChoiceListView(ListView):
    context_object_name = "choices"
    queryset = Choice.objects.all()
    template_name = "polls/choices.html"


class ChoiceDetailView(DetailView):
    queryset = Choice.objects.all()
    template_name = "polls/choice_detail.html"
    pk_url_kwarg = "choice_id"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["choice_poll"] = self.poll
    #     return context                                             


    # def get_object(self):
    #     obj = super().get_object()
    #     obj.choice_poll = self.get_context_data("choice_poll")
    #     obj.save()
    #     return obj







def home(request,catslug=None,sc=None,sort_by=None):
    
    categories = Category.objects.all().order_by('-polls_count')
    
    # to save the polls count for each category in database 
    for cat in categories :
        polls = Poll.objects.all().filter(category=cat)
        polls_count = polls.count()
        cat.polls_count = polls_count
        cat.save()
    
    
    polls = Poll.objects.all()
    
    # to delete from database any poll which has no choice  -- cleaning database from wrong polls
    for poll in polls:
        print(poll.choice_set.count())
        if poll.choice_set.count() == 0 or  poll.choice_set.count() < int(5) :
           poll.delete()
        
        
    latest_poll_list = polls.order_by('-published_at')
    
    # search poll by poll_question 
    if 'sc' in request.GET  :   
        sc = request.GET['sc']
        if sc != "" :
            latest_poll_list = latest_poll_list.filter(poll_descript__icontains=sc) 
        
    
    # filter by category
    if catslug != None:
       latest_poll_list   = latest_poll_list.filter(category__slug=catslug)
    
        

    # sort by :
    if sort_by != None:
        if sort_by == 'PUB':
            latest_poll_list  = latest_poll_list.order_by('-published_at')
        if sort_by == 'VOT':
             latest_poll_list = latest_poll_list.order_by('-poll_voters_count')
        if sort_by == 'ALPH':
            latest_poll_list  = latest_poll_list.order_by('poll_question')
        
        
    
    context = {
        'title'              : 'Home',
        'description_content': 'Home page list all polls',
        'categories'      : Category.objects.all().order_by('-polls_count') ,
        'latest_poll_list': latest_poll_list,
        'sc'                : sc ,
        }
    return render(request, 'polls/home.html', context)




@login_required(login_url='users:user-login')
def poll_create(request):
    form = PollForm()
    if request.method =='POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll= form.save(commit=False)
            poll.poll_user = request.user
            poll.save()
            messages.success(request,f'Thank you {request.user.username} now you must add choices for this poll.')
            return HttpResponseRedirect(reverse('polls:poll-choices-create', kwargs={"poll_slug": poll.poll_slug,
                                                                                    "year": poll.published_at.year,
                                                                                   "month": poll.published_at.month,
                                                                                     "day": poll.published_at.day}))
            
        else:
            form = PollForm()
            messages.error(request, f'error in creating a poll please try again!') 
    
    context ={
        'title'              : 'Poll Create',
        'description_content': 'Add a new poll for the selected Category',
        'form':form,    
    }
    return render(request,'polls/poll_create.html', context)








@login_required(login_url='users:user-login')
def poll_choices_create(request,poll_slug,year,month,day):
    # poll = get_object_or_404(Poll, poll_slug=poll_slug,
    #                       published_at__year=year,
    #                      published_at__month=month,
    #                        published_at__day=day)
    
    poll = Poll.objects.filter(poll_slug=poll_slug,
                          published_at__year=year,
                         published_at__month=month,
                           published_at__day=day).first()
    
    
    form = ChoiceForm()
    if request.method =='POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice= form.save(commit=False)
            choice.choice_poll = poll
            choice.save()
            if poll.choice_set.count() == 0 :
                poll.delete()
            messages.success(request,f'Thank you {request.user.username} for adding choice to this poll.')
            return HttpResponseRedirect(reverse('polls:poll-choices-create', kwargs={"poll_slug": poll.poll_slug,
                                                                                    "year": poll.published_at.year,
                                                                                   "month": poll.published_at.month,
                                                                                     "day": poll.published_at.day}))
        else:    
            form = ChoiceForm()
            messages.error(request, f'error in creating a choice please try again!') 
    context = {
        'title'              : 'Poll Choices Create',
        'description_content': 'Create the choices for the selected poll',
        'poll'       : poll,
        'poll_form'  : form,    
    }
    return render(request, 'polls/poll_choices_create.html', context)





@login_required(login_url='users:user-login')
def poll_update(request,year,month,day,poll_slug): 
    poll = get_object_or_404(Poll, status=Poll.Status.PUBLISHED,
                                    poll_slug=poll_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    if poll.poll_user == request.user or request.user.role == 'ADMIN' :
        #-----PollForm()-------#  
        poll_form = PollForm(instance=poll)
        if request.method == 'POST':
            poll_form = PollForm(request.POST,request.FILES,instance=poll)
            if poll_form.is_valid():
                updated_poll = poll_form.save(commit=False)
                updated_poll.poll_user = request.user
                updated_poll.save() 
                messages.success(request,f'Thanks ( {request.user.username} ), your poll updated successfully !')
                return redirect('polls:poll-choices-create',year=poll.published_at.year,month=poll.published_at.month,day=poll.published_at.day,poll_slug=poll.poll_slug)
            
         
            
            else:
                poll_form = PollForm(request.POST,request.FILES,instance=poll)
                messages.error(request,f'Poll not update correctly! please try again.!')
             
    
    else:
        messages.warning(request,f"Sorry, you have no permission to update this posll, only poll's author can update it")
        return redirect('polls:home')
    
    context ={
        'title'       :'Poll Update',
        'description_content': 'Update the selected poll',
        'poll'        : poll,
        'poll_form'   : poll_form,
        
    }
    return render(request,'polls/poll_update.html',context)




@login_required(login_url='users:user-login')
def poll_choices_update(request,year,month,day,poll_slug,choice_id): 
    poll = get_object_or_404(Poll, status=Poll.Status.PUBLISHED,
                                    poll_slug=poll_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    
    choice = Choice.objects.filter(choice_poll=poll,id=choice_id).first()
    print(choice)
    if poll.poll_user == request.user or request.user.role == 'ADMIN' :
        #---- ChoiceForm()-------#  
        choice_form = ChoiceForm(instance=choice)
        if request.method == 'POST':
            choice_form = ChoiceForm(request.POST,request.FILES,instance=choice)
            if choice_form.is_valid():
                updated_choice = choice_form.save(commit=False)
                updated_choice.choice_poll = poll
                updated_choice.id = choice_id
                updated_choice.save() 
                messages.success(request,f'Thanks ( {request.user.username} ),the choice updated successfully !')
                return redirect('polls:poll-choices-create',year=poll.published_at.year,month=poll.published_at.month,day=poll.published_at.day,poll_slug=poll.poll_slug)
            
         
            
            else:
                choice_form = ChoiceForm(choice.id,request.POST,request.FILES)
                messages.error(request,f'choice not update correctly! please try again.!')
             
        # #-----ChoiceForm()-------#      
        # for choice in poll.choice_set.all() :
        #     choice_form = ChoiceForm(instance=choice)
             
    
    else:
        messages.warning(request,f"Sorry, you have no permission to update , only poll's author can update it")
        return redirect('polls:home')
    
    context ={
        'title'               :'Choice Update',
        'description_content' : 'Update choice for the selected poll',
        'poll'                : poll,
        'choice_form'         : choice_form,
        
    }
    return render(request,'polls/poll_choices_update.html',context)





@login_required(login_url='users:user-login')
def poll_delete_confirm(request,year,month,day,poll_slug):
    poll = get_object_or_404(Poll, status=Poll.Status.PUBLISHED,
                                    poll_slug=poll_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    if poll.poll_user == request.user or request.user.role == 'ADMIN':
        if request.method == 'POST' and 'yes-delete' in request.POST:
            poll.delete()
            messages.success(request,f'Thanks ( {request.user.username} ), your poll deleted successfully !')
            return redirect('polls:home')
             
                
        context ={
            
            'title'               : 'Poll Delete Confirm',
            'description_content' : 'Delete selected poll',
            'poll'                :  poll ,
        }
        return render(request,'polls/poll_delete_confirm.html',context)
 
    else:
        messages.warning(request,f"Sorry, you have no permission to delete this poll, only poll's author can delete it")
        return redirect('polls:home')
    






def poll_detail(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                          published_at__year=year,
                         published_at__month=month,
                           published_at__day=day
    )
    context = {
        'title'              : 'Poll Detail',
        'description_content': 'poll detail page',
        'poll': poll
    }
    return render(request, 'polls/poll_detail.html', context)






@login_required(login_url='users:user-login')
def poll_vote_create(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    
    user = request.user
    if user in poll.poll_voters.all():
        messages.error(request,f"Sorry, you have no permission to vote again on the same poll !")
        return redirect('polls:poll-votes-result',year=poll.published_at.year,month=poll.published_at.month,day=poll.published_at.day,poll_slug=poll.poll_slug)
        
    
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        selected_choice.choice_votes_count += 1
        selected_choice.save()
        poll.poll_voters.add(user)
        poll.poll_voters_count = poll.poll_voters.count()
        poll.save()
        
        
            
        return HttpResponseRedirect(reverse('polls:poll-votes-result', kwargs={"poll_slug": poll.poll_slug,
                                                                                    "year": poll.published_at.year,
                                                                                   "month": poll.published_at.month,
                                                                                     "day": poll.published_at.day}))
    
    except (KeyError, Choice.DoesNotExist):
        
        context={
            'title'              : 'Vote Create',
            'description_content': 'Vote create for the poll',
            'poll': poll,
            'message': "You didn't select a choice.",   
        
        }
        return render(request, 'polls/poll_detail.html', context)
    




def poll_votes_result(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    poll_choices_labels  = []
    poll_choices_votes_counts = []
    choices = poll.choice_set.all()
    for choice in choices :
        poll_choices_labels.append(choice.choice_text)
        poll_choices_votes_counts.append(choice.choice_votes_count)
           
    context={
        'title'              : 'Poll Votes result',
        'description_content': "Display the votes result of the poll with displaying chart",
        'poll': poll,
        'labels' : poll_choices_labels,
        'data_count'  : poll_choices_votes_counts 
        
    }
    return render(request, 'polls/poll_votes_result.html', context)   




def poll_share_by_email(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    form = SharePollByEmailForm()
    if request.method == 'POST':
        form = SharePollByEmailForm(request.POST)
        # print("form"+ str(form))
        if form.is_valid():
            cd = form.cleaned_data
            print("cd="+ str(cd))
            sender_name = cd.get('sender_name')
            sender_email = cd.get('sender_email')
            recipient_email = cd.get('recipient_email')
            sender_comment = cd.get('sender_comment')
            
            # https://docs.djangoproject.com/en/4.2/topics/email/#send-mail
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)¶
            subject = f"{sender_name} recommends you read {poll.poll_descript}"
            poll_url = request.build_absolute_uri(poll.get_absolute_url())
            message = f"Isuggest to you to do votes at ({poll.poll_descript}) at {poll_url} \n {sender_name}\'s comments:{sender_comment}"
            from_email =  sender_email
            recipient_list = [recipient_email]
            send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            print("send_mail=",send_mail(subject,message,from_email,recipient_list))
            messages.success(request,f'Thanks ( {sender_name} ), for sharing the post ({poll.poll_descript}).')
            return redirect('polls:poll-detail',year=poll.published_at.year,month=poll.published_at.month,day=poll.published_at.day,poll_slug=poll.poll_slug)
    
        else:
            form = SharePollByEmailForm()
            messages.error(request,f'The post ({poll.poll_descript}) not shared! please try again')
            
    else:
        form = SharePollByEmailForm()
    
    context = {
        'title': 'Poll Share By Email',
        'description_content': 'Share the poll by email',
        'poll' : poll,
        'form' : form,
    }
    return  render(request,'polls/poll_share.html',context=context)       
















################################################### Google Search Console #############################3333333333

#  https://search.google.com/search-console  
############################# Google Search Console - google-site-verification  #############################
from django.http import HttpResponse
from django.views import View

class GoogleSiteVerificationView(View):
    line  =  "google-site-verification: google7a03622cb96e4f8f.html"
    
    def get(self, request, *args, **kwargs):
        return HttpResponse(self.line)