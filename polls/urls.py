from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # Category
    path('categories/', views.categories, name='categories'),
    path('cat-detail/<slug:cat_slug>/', views.cat_detail, name='cat-detail'),
    
   
    
    # Polls
    path('', views.home, name='home'),
    # polls #home sort by  # order_by
    path('sort/<str:sort_by>/', views.home, name='home-sort-by'),
    # polls # home filte by category
    path('cat/<slug:catslug>/', views.home, name='home-filter-category'),
    path('new-poll/', views.poll_create, name='poll-create'),
    path('poll-choices-create/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_choices_create, name='poll-choices-create'),
    path('poll-choices-update/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/<int:choice_id>/',views.poll_choices_update, name='poll-choices-update'),
    path('poll-detail/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_detail, name='poll-detail'),
    path('poll-update/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_update, name='poll-update'),
    path('poll-delete-confirm/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_delete_confirm, name='poll-delete-confirm'),
    path('poll-votes-result/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_votes_result, name='poll-votes-result'),
    path('poll-vote-create/<slug:poll_slug>/<int:year>/<int:month>/<int:day>/', views.poll_vote_create, name='poll-vote-create'),
    # path('poll-like/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.poll_like_action, name='poll-like'),
    # path('poll-share-by-email/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.poll_share_by_email, name='poll-share-by-email'), 
]



    