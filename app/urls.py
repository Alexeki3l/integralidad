from django.urls import path
from app.views.actividades import list_activities, DetailsActivityView, EditActivityView, DeleteActivityView, AddActivityView
from app.views.profile import list_roles, DetailsProfileView, EditProfileView, list_roles_by_rol
from app.views.activity_and_student import AddActivityAndStudentView, list_activity_and_student_for_profesor\
    ,DetailsActivityAndStudentForProfessorView, ActivityAndStudentUpdateView
    
from app.views.caracterizacion import caracterizacion, evaluacion_integral_student, exportar_pdf_student


# from ..authentication.views import update_data

urlpatterns = [
    # ...Actividades....
    path('list_activities/', list_activities, name='list_activities'),
    
    path('add_activities/', AddActivityView.as_view(), name='add_activities'),
    path('details_activity/<int:pk>', DetailsActivityView.as_view(), name='details_activity'),
    path('edit_activity/<int:pk>', EditActivityView.as_view(), name='edit_activity'),
    path('delete_activity/<int:pk>', DeleteActivityView.as_view(), name='delete_activity'),
    #
    
    # Activity And Student
    path('add_activities_and_student/<int:pk>', AddActivityAndStudentView.as_view(), name='add_activities_and_student'),
    path('list_activity_and_student_for_profesor/<int:pk_student>', list_activity_and_student_for_profesor, name='list_activity_and_student_for_profesor'),
    path('activity_and_student_update/<int:pk_activity_int>', ActivityAndStudentUpdateView.as_view(), name='activity_and_student_update'),
    
    path('details_activity_and_student_for_profesor/<int:pk_student>/<int:pk_activity>', DetailsActivityAndStudentForProfessorView.as_view(), name='details_activity_and_student_for_profesor'),
    
    
    
    # Caracterizacion
    path('caracterizacion', caracterizacion, name='caracterizacion_pk_student'),
    path('caracterizacion/evaluacion_integral', caracterizacion, name='evaluacion_integral'),
    path('caracterizacion/exportar_pdf', caracterizacion, name='exportar_pdf'),
    
    path('caracterizacion/evaluacion_integral_student/<int:pk_student>', evaluacion_integral_student, name='evaluacion_integral_student'),
    path('caracterizacion/exportar_pdf_student/<int:pk_student>', exportar_pdf_student, name='exportar_pdf_student'),
    
    # ...Roles
    
    path('roles/<int:id_rol>', list_roles, name='list_roles'),
    path('details_rol/<int:pk>', DetailsProfileView.as_view(), name='details_rol'),
    path('edit_rol/<int:pk>', EditProfileView.as_view(), name='edit_rol'),
    
    path('roles/list_roles_by_rol/<int:id_profile>', list_roles_by_rol, name='list_roles_by_rol')
    
]