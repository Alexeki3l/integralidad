from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('', views.activities, name='activities'),
    path('search_activities/', views.search_activities, name='search_activities'),
    path('add_activities/', views.AddActivityView.as_view(), name='add_activities'),
    path('details_activity/<int:pk>', views.DetailsActivityView.as_view(), name='details_activity'),
    path('edit_activity/<int:pk>', views.EditActivityView.as_view(), name='edit_activity'),
    path('delete_activity/<int:pk>', views.DeleteActivityView.as_view(), name='delete_activity'),
    # ...
]