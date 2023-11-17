from django.urls import path
from . import views

# from ..authentication.views import update_data

urlpatterns = [
    # ...Actividades....
    path('', views.list_activities, name='list_activities'),
    
    # path('', views.list_activities, name='list_activities'),
    # path('list_activities_htmx/', views.list_activities_htmx, name='list_activities_htmx'),
    # path('search_activities/', views.search_activities, name='search_activities'),
    path('add_activities/', views.AddActivityView.as_view(), name='add_activities'),
    
    path('details_activity/<int:pk>', views.DetailsActivityView.as_view(), name='details_activity'),
    path('edit_activity/<int:pk>', views.EditActivityView.as_view(), name='edit_activity'),
    path('delete_activity/<int:pk>', views.DeleteActivityView.as_view(), name='delete_activity'),
    #
    
    # Activity And Student
    path('add_activities_and_student/<int:pk>', views.AddActivityAndStudentView.as_view(), name='add_activities_and_student'),
    
    # ...Roles
    
    path('roles/<int:id_rol>', views.list_roles, name='list_roles'),
    path('details_rol/<int:pk>', views.DetailsProfileView.as_view(), name='details_rol'),
    path('edit_rol/<int:pk>', views.EditProfileView.as_view(), name='edit_rol'),
]