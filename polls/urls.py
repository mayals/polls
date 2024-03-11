from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:question_slug>/<int:year>/<int:month>/<int:day>/', views.question_detail, name='question-detail'),
    path('question-votes-result/<slug:question_slug>/<int:year>/<int:month>/<int:day>/', views.question_votes_result, name='question-votes-result'),
    path('question-vote-create/<slug:question_slug>/<int:year>/<int:month>/<int:day>/', views.question_vote_create, name='question-vote-create'),
]