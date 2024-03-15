from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('contact-us/', views.contact_us, name='contact-us'),
    path('thank-you/', views.ThankTemplateView.as_view(), name='thank-you'),
    path('about/', views.AboutTemplateView.as_view(), name='about'),
    path('privacy-police/', views.LicenceTemplateView.as_view(), name='licence'),


]