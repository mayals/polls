from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_detail, name='poll-detail'),
    path('poll-votes-result/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_votes_result, name='poll-votes-result'),
    path('poll-vote-create/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_vote_create, name='poll-vote-create'),
]