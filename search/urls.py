from django.urls import path
from . import views

urlpatterns = [
    path('search/<int:class_id>', views.search, name='search'),
    path('search/<int:class_id>/history/', views.search_history, name='search_history'),
]
