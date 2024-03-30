from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# sitemaps
from django.contrib.sitemaps import GenericSitemap  # new
from django.contrib.sitemaps.views import sitemap  # new
from polls.sitemap import StaticSitemap, PollSitemap, CategorySitemap, ChoiceSitemap 
from django.views.generic import TemplateView




sitemaps = {
    'static'     : StaticSitemap,
    'polls'      : PollSitemap,
    'categories' : CategorySitemap,
    'choices'    : ChoiceSitemap,
}

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # polls 
    path('',include('polls.urls', namespace='polls')),
    
    # users
    path('users/',include('users.urls', namespace='users')),
    
    # pages
    path('pages/',include('pages.urls', namespace='pages')),
    
    # https://pypi.org/project/django-tinymce/
    path('tinymce/', include('tinymce.urls')),
    
    # https://docs.djangoproject.com/en/5.0/ref/contrib/sitemaps/#module-django.contrib.sitemaps
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









# 404  page
handler404 = 'pages.views.handling_404'






# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)