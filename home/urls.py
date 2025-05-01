from django.urls import path
from . import views
from .views import landing_page, home_view

urlpatterns = [
    path('', landing_page, name='landing'),            # Landing shown at /
    path('home/', home_view, name='home'),             # Home shown at /home/
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
