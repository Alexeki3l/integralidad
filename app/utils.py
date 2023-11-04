def return_list_activities_html(activities):
    """Se encarga de iterar la lista de actividades enviada por parametro y retorna una 
    estructura en html lista para enviarse al template"""
    
    list_aux = [f"""<tr>
                                                        <td>{activity.description}</td>
                                                        <td>{activity.aspecto}</td>
                                                        <td>{activity.is_open}</td>
                                                        <td class="table-action">
                                                            <a href="details_activity/{activity.pk}" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                            <a href="edit_activity/{activity.pk}" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                            <a href="delete_activity/{activity.pk}" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                        </td>
                                                    </tr>""" for activity in activities]
    
    
    return list_aux


def return_content_full_table_html(activities):
    """Se encarga de iterar la lista de actividades enviada por parametro y retorna una 
    estructura en html lista para enviarse al template"""
    
    head = """<table id="basic-datatable" class="table dt-responsive nowrap w-100">
                                <thead>
                                    <tr>
                                        <th>Nombre</th>
                                        <th>Aspecto</th>
                                        <th>Activa?</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                
                                <tbody id="search-results">"""
    
    list_aux = "".join([f"""<tr>
                                                        <td>{activity.description}</td>
                                                        <td>{activity.aspecto}</td>
                                                        <td>{activity.is_open}</td>
                                                        <td class="table-action">
                                                            <a href="details_activity/{activity.pk}" class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                            <a href="edit_activity/{activity.pk}" class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                            <a href="delete_activity/{activity.pk}" class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                        </td>
                                                    </tr>""" for activity in activities])
    
    footer = """</tbody>
                                
                            </table>  """
                            
    result = head + list_aux + footer
    
    return result

def elements_footer_table():
    html = """<div class="row justify-content-between my-2">
                            <div class="col-4">
                                Mostrando {{begin}} a {{end}} de {{count_total_objects}} entradas
                            </div>
                            <div class="col-3">
                                <nav aria-label="Page navigation example">
                                    <ul class="pagination pagination-sm justify-content-end">
                                        {% if anterior < 0 %}
                                        <li class="page-item disabled">
                                            <a href="#" class="page-link">Anterior</a>
                                        </li>
                                        {% else %}
                                        <li class="page-item ">
                                            <a href="{% url "activities" anterior %}" class="page-link">Anterior</a>
                                        </li>
                                        {% endif %}

                                        {% for number_page in pages %}
                                            <li class="page-item {% if number_page|stringformat:"d" in request.path %} disabled {% endif %}" ><a class="page-link" href="{% url "activities" number_page %}">{{number_page|add:1}}</a></li>
                                        {% endfor %}
                                        
                                        {% if siguiente == 0 %}
                                            <li class="page-item disabled"><a class="page-link" href="#">Siguiente</a>
                                        {% else %}
                                            {% comment %} <li class="page-item"><a class="page-link" href="{% url "activities" siguiente %}">Siguiente</a> {% endcomment %}
                                                <li class="page-item">
                                                    <a  name="siguiente"
                                                        href="{% url "activities" siguiente %}"
                                                        hx-get="{% url "activities" siguiente %}" 
                                                        hx-trigger="click" 
                                                        hx-target="#basic-datatable-preview" 
                                                        hx-swap="innerHTML"
                                                        class="page-link"
                                                        >Siguiente</a>
                                                </li>
                                        {% endif %}
                                        
                                      </li>
                                    </ul>
                                </nav>
                            </div>
                        </div> """
    return html