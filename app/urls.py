from django.urls import path
from . import views

urlpatterns = [
    # ...
   
    path('', views.list_activities, name='list_activities'),
    path('list_activities_htmx/', views.list_activities_htmx, name='list_activities_htmx'),
    # path('search_activities/', views.search_activities, name='search_activities'),
    path('add_activities/', views.AddActivityView.as_view(), name='add_activities'),
    
    path('details_activity/<int:pk>', views.DetailsActivityView.as_view(), name='details_activity'),
    path('edit_activity/<int:pk>', views.EditActivityView.as_view(), name='edit_activity'),
    path('delete_activity/<int:pk>', views.DeleteActivityView.as_view(), name='delete_activity'),
    #
    path('activities/details_activity/<int:pk>', views.DetailsActivityView.as_view(), name='details_activity'),
    path('activities/edit_activity/<int:pk>', views.EditActivityView.as_view(), name='edit_activity'),
    path('activities/delete_activity/<int:pk>', views.DeleteActivityView.as_view(), name='delete_activity'),
    # ...
]