from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Poll, Choice
from .forms import PollForm,ChoiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    latest_poll_list = Poll.objects.order_by('-published_at')[:5]
    context = {
        'latest_poll_list': latest_poll_list
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
            messages.success(request,f'Thank you {request.user.username}now you must add choices for this poll.')
            return HttpResponseRedirect(reverse('polls:poll-choices-create', kwargs={"poll_slug": poll.poll_slug,
                                                                                    "year": poll.published_at.year,
                                                                                   "month": poll.published_at.month,
                                                                                     "day": poll.published_at.day}))
            
        else:
            form = PollForm()
            messages.error(request, f'error in creating a poll please try again!') 
    context ={
        'form':form,    
    }
    return render(request,'polls/poll_create.html', context)



@login_required(login_url='users:user-login')
def poll_choices_create(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                          published_at__year=year,
                         published_at__month=month,
                           published_at__day=day)
    
    
    form = ChoiceForm()
    if request.method =='POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice= form.save(commit=False)
            choice.choice_poll = poll
            choice.save()
            messages.success(request,f'Thank you {request.user.username}now you add choice for this poll.')
            return HttpResponseRedirect(reverse('polls:poll-choices-create', kwargs={"poll_slug": poll.poll_slug,
                                                                                    "year": poll.published_at.year,
                                                                                   "month": poll.published_at.month,
                                                                                     "day": poll.published_at.day}))
        else:    
            form = ChoiceForm()
    context = {
        'poll'  : poll,
        'form'  : form,    
    }
    return render(request, 'polls/poll_choices_create.html', context)










@login_required(login_url='users:user-login')
def poll_delete_confirm(request,year,month,day,poll_slug):
    poll = get_object_or_404(Poll, status=Poll.Status.PUBLISHED,
                                    poll_slug=poll_slug, 
                                    published_at__year=year,
                                    published_at__month=month,
                                    published_at__day=day,
    ) 
    if poll.poll_user == request.user :
        if request.method == 'POST' and 'yes-delete'in request.POST:
            poll.delete()
            messages.success(request,f'Thanks ( {request.user.username} ), your poll deleted successfully !')
            return redirect('polls:home')
                
        context ={
            'title': 'Poll Delete Confirm',
            'poll' :  poll ,
        }
        return render(request,'polls/poll_delete_confirm.html',context)
 
    else:
        messages.warning(request,f"Sorry, you have no permission to delete this poll, only poll's author can delete it")
        return redirect('polls:home')
    





@login_required(login_url='users:user-login')
def poll_vote_create(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        selected_choice.choice_votes_count += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:poll-votes-result', kwargs={"poll_slug": poll.poll_slug,
                                                                                    "year": poll.published_at.year,
                                                                                   "month": poll.published_at.month,
                                                                                     "day": poll.published_at.day}))
    
    except (KeyError, Choice.DoesNotExist):
        context={
            'poll': poll,
            'error_message': "You didn't select a choice.",   
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
        'poll': poll,
        'labels' : poll_choices_labels,
        'data_count'  : poll_choices_votes_counts 
        
    }
    return render(request, 'polls/poll_votes_result.html', context)        




def poll_detail(request,poll_slug,year,month,day):
    poll = get_object_or_404(Poll, poll_slug=poll_slug,
                          published_at__year=year,
                         published_at__month=month,
                           published_at__day=day
    )
    context = {
        'poll': poll
    }
    return render(request, 'polls/poll_detail.html', context)


