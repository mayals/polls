from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # polls 
    path('polls/',include('polls.urls', namespace='polls')),
]
