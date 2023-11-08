from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.data_view, name='data_projects'),
    path('export-csv/', views.export_csv, name='export_csv'),
]