from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    # polls 
    path('',include('polls.urls', namespace='polls')),
    # users
    path('users/',include('users.urls', namespace='users')),
    # pages
    path('pages/',include('pages.urls', namespace='pages'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'pages.views.handling_404'



# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)