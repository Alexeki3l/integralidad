from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('', views.home, name='home'),
    path('/search_activities', views.search_activities, name='search_activities'),
    # ...
]