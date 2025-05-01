# urls.py (within the lost_items app)
from django.urls import path
from . import views
from .views import export_lost_items_csv


app_name = 'lost_items'

urlpatterns = [
    path('report-lost-item/', views.report_lost_item, name='report_lost_item'),
    path('search-lost-items/', views.search_lost_items, name='search_lost_items'),  # Search lost items
    path('lost-item/<int:pk>/', views.lost_item_detail, name='lost_item_detail'),
    path('toggle-status/<int:pk>/', views.toggle_lost_item_status, name='toggle_lost_status'),
    path('download-lost-items/', export_lost_items_csv, name='download_lost_items_csv'), # Lost item detail
]
