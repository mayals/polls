from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Poll, Choice


def home(request):
    latest_poll_list = Poll.objects.order_by('-published_at')[:5]
    context = {
        'latest_poll_list': latest_poll_list
        }
    return render(request, 'polls/home.html', context)





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
    

        