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


def return_content_full_table_html(activities, begin, end, count_total_objects, anterior, siguiente):
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
                            
    result = head + list_aux + footer + elements_footer_table(begin, end, count_total_objects, anterior, siguiente)
    
    return result

def elements_footer_table(begin, end, count_total_objects, anterior, siguiente):
    
    if anterior < 0:
        anterior_html = """<li class="page-item disabled">
                                <a href="#" class="page-link">Anterior</a>
                            </li>"""
    else:
        anterior_html = """<li class="page-item ">
                                <a href="{% url "activities" anterior %}" class="page-link">Anterior</a>
                            </li>"""
                            
    if siguiente < 0:
        siguiente_html = """<li class="page-item disabled"><a class="page-link" href="#">Siguiente</a>"""
    else:
        
        url_django = f"""list_activities_htmx/"""
        siguiente_html = f"""<li class="page-item">
                                <a  name="siguiente"
                                    href="{url_django}"
                                    hx-get="{url_django}" 
                                    hx-trigger="click" 
                                    hx-target="#basic-datatable-preview" 
                                    hx-swap="innerHTML"
                                    class="page-link"
                                >Siguiente</a>
                            </li>"""
    
    html = f"""<div class="col-3">
                <nav aria-label="Page navigation example">
                    <ul class="pagination pagination-sm justify-content-end">
                        {anterior_html}

                        {siguiente_html}
                    </ul>
                </nav>
            </div>"""
    html_1 = f"""<div class="row justify-content-between my-2">
                            <div class="col-4">
                                Mostrando {begin} a {end} de {count_total_objects} entradas
                            </div>
                            {html}
                        </div> """
    
    return html_1

def delete_key_values_in_cookies(response, key, value=''):
    try:
        response.set_cookie(key, value, expires='Thu, 01 Jan 1970 00:00:00 GMT')
        # return True
    except:
        pass
    
def data_page(begin, end, total):
    cadena = f"Mostrando {begin} a {end} de {total} entradas"
    return cadena
    
    
    
# def html_content(activities):
    
#     html = """
#         <div class="row justify-content-between">
#                             <div class="col-4">
#                                 {% comment %} <div class="row">
#                                     <div class="col-auto">
#                                         Mostar
#                                     </div>
#                                     <div class="col-auto px-0">
#                                         <select class="form-select form-select-sm" aria-label="Small select example">
#                                             <option value="1">10</option>
#                                             <option value="2">20</option>
#                                             <option value="3">50</option>
#                                           </select>
#                                     </div>
#                                     <div class="col-auto">
#                                         entradas
#                                     </div>
#                                   </div> {% endcomment %}
#                             </div>
#                             <div class="col-3">
                                
#                                 <input class="form-control form-control-sm" type="search" 
#                                 name="search_activities" placeholder="Buscar..." 
#                                 hx-get="{% url "activities_htmx" %}" 
#                                 hx-trigger="keyup changed delay:500ms, search" 
#                                 hx-target="#basic-datatable-preview" 
#                                 hx-swap="innerHTML"
#                                 {% comment %} hx-indicator=".htmx-indicator" {% endcomment %}
#                                 >
#                             </div>
#                         </div>
#     """
#     html += """
#         <div class="tab-pane show active my-3" id="basic-datatable-preview">
#     """
    
#     table = return_content_full_table_html(activities)
    
#     html += table
    
#     html += """
#         </div>
#     """
    
#     html += elements_footer_table()
    
#     return html
    
    
    