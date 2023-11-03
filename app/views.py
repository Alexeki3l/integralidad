from django.shortcuts import render, redirect
from .models import Activity, Aspecto
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

def activities(request):
    if request.user.is_authenticated:
        activities = Activity.objects.all()
        if request.htmx:
            if request.htmx.target == 'search-results':
                search_input = request.GET.get('search_activities', None)
                if search_input:
                    # print(request.path)
                    
                    patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
                    activities = activities.filter(patterns)
                    
                    return HttpResponse(
                            [f"""<tr>
                                                        <td>{activity.description}</td>
                                                        <td>{activity.aspecto}</td>
                                                        <td>{activity.is_open}</td>
                                                        <td class="table-action">
                                                            <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                            <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                            <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                        </td>
                                                    </tr>""" for activity in activities]
                        )
                    # else:
                    #     return HttpResponse(
                    #         '<p class="text-center">Center aligned text on all viewport sizes.</p>'
                    #         )
                else:
                    # activities = Activity.objects.all()
                    return HttpResponse(
                        [f"""<tr>
                                                    <td>{activity.description}</td>
                                                    <td>{activity.aspecto}</td>
                                                    <td>{activity.is_open}</td>
                                                    <td class="table-action">
                                                        <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                        <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                        <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                    </td>
                                                </tr>""" for activity in activities])
            
        context = {
            'actividades': activities,
            'flag': True
        }
        return render(request, 'actividad.html', context=context)
    else:
        return redirect('login')
    
    
def search_activities(request):
    search_input = request.GET.get('search_activities', None)
    if search_input:
        # print(request.path)
        
        patterns =Q(description__icontains=search_input) | Q(aspecto_id__in=Aspecto.objects.filter(name__icontains = search_input).values_list('id', flat=True))
        activities = Activity.objects.filter(patterns).all()
        
        return HttpResponse(
                [f"""<tr>
                                            <td>{activity.description}</td>
                                            <td>{activity.aspecto}</td>
                                            <td>{activity.is_open}</td>
                                            <td class="table-action">
                                                <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                            </td>
                                        </tr>""" for activity in activities]
            )
        # else:
        #     return HttpResponse(
        #         '<p class="text-center">Center aligned text on all viewport sizes.</p>'
        #         )
    else:
        activities = Activity.objects.all()
        return HttpResponse(
            [f"""<tr>
                                        <td>{activity.description}</td>
                                        <td>{activity.aspecto}</td>
                                        <td>{activity.is_open}</td>
                                        <td class="table-action">
                                            <a href="javascript: void(0);" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                            <a href="javascript: void(0);" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                            <a href="javascript: void(0);" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                        </td>
                                    </tr>""" for activity in activities])
