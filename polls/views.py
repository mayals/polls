from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


def home(request):
    latest_question_list = Question.objects.order_by('-published_at')[:5]
    context = {
        'latest_question_list': latest_question_list
        }
    return render(request, 'polls/home.html', context)



def question_detail(request,question_slug,year,month,day):
    question = get_object_or_404(Question, slug=question_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    context = {
        'question': question
    }
    return render(request, 'polls/question_detail.html', context)





def question_votes_result(request,question_slug,year,month,day):
    question = get_object_or_404(Question, slug=question_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    question_choices_labels  = []
    question_choices_votes_counts = []
    choices = question.choice_set.all()
    for choice in choices :
        question_choices_labels.append(choice.choice_text)
        question_choices_votes_counts.append(choice.choice_votes_count)
        
        
        
    context={
        'question': question,
         'labels' : question_choices_labels,
          'data_count'  : question_choices_votes_counts 
        
    }
    return render(request, 'polls/question_votes_result.html', context)





def question_vote_create(request,question_slug,year,month,day):
    question = get_object_or_404(Question, slug=question_slug,
                                published_at__year=year,
                                published_at__month=month,
                                published_at__day=day
    )
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.choice_votes_count += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:question-votes-result', kwargs={"question_slug": question.slug,
                                                                                            "year": question.published_at.year,
                                                                                           "month": question.published_at.month,
                                                                                             "day": question.published_at.day}))
    
    
    except (KeyError, Choice.DoesNotExist):
        context={
            'question': question,
            'error_message': "You didn't select a choice.",   
        }
        return render(request, 'polls/question_detail.html', context)
    

        