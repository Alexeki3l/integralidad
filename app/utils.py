def return_list_activities_html(activities):
    """Se encarga de iterar la lista de actividades enviada por parametro y retorna una 
    estructura en html lista para enviarse al template"""
    
    apertura = "{% url"
    cierre = "%}"
    list_aux = [f"""<tr>
                                                        <td>{activity.description}</td>
                                                        <td>{activity.aspecto}</td>
                                                        <td>{activity.is_open}</td>
                                                        <td class="table-action">
                                                            <a href='details_activity/{activity.pk}' class="action-icon text-success"> <i class="mdi mdi-eye"></i></a>
                                                            <a href='edit_activity/{activity.pk}' class="action-icon text-primary"> <i class="mdi mdi-pencil"></i></a>
                                                            <a href='delete_activity/{activity.pk}' class="action-icon text-danger"> <i class="mdi mdi-delete"></i></a>
                                                        </td>
                                                    </tr>""" for activity in activities]
    
    
    return list_aux