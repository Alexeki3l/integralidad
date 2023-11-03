from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('', views.activities, name='activities'),
    path('search_activities/', views.search_activities, name='search_activities'),
    # ...
]