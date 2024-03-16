from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # polls 
    path('',include('polls.urls', namespace='polls')),
    # users
    path('users/',include('users.urls', namespace='users')),
    # pages
    path('pages/',include('pages.urls', namespace='pages'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)