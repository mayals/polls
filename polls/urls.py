from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # polls
    path('', views.home, name='home'),
    path('new-poll/', views.poll_create, name='poll-create'),
    path('poll-choices-create/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_choices_create, name='poll-choices-create'),
    path('poll-detail/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_detail, name='poll-detail'),
    #path('poll-update/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_update, name='poll-update'),
    path('poll-delete-confirm/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_delete_confirm, name='poll-delete-confirm'),
    path('poll-votes-result/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_votes_result, name='poll-votes-result'),
    path('poll-vote-create/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_vote_create, name='poll-vote-create'),
    # path('poll-like/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.poll_like_action, name='poll-like'),
    # path('poll-share-by-email/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.poll_share_by_email, name='poll-share-by-email'), 
]



    