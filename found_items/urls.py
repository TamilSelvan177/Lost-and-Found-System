# urls.py (within the found_items app)
from django.urls import path
from . import views

app_name = 'found_items'

urlpatterns = [
    path('report-found-item/', views.report_found_item, name='report_found_item'),
    path('search-found-items/', views.search_found_items, name='search_found_items'),  # Search found items
    path('found-item/<int:pk>/', views.found_item_detail, name='found_item_detail'),
    path('toggle-status/<int:pk>/', views.toggle_found_item_status, name='toggle_found_status'),  # Toggle status
]
