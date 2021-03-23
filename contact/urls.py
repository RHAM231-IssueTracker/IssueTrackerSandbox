from django.urls import path
from . import views

# Manages the url for the contact page.
# First value displays in the internet search bar.
# Second value accesses the related view.
# "name" is what is called out in templates.
urlpatterns = [
    path('', views.contact, name='contact-us'),
]
