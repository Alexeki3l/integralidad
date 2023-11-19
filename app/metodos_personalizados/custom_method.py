def order_list_by_group(lista):
    def key_function(item):
    # La clave es el número que aparece en el medio de cada cadena
        return int(item[3:7])

    # Ordena la lista utilizando la función de clave personalizada
    sorted_list = sorted(lista, key=key_function)

    # Imprime la lista ordenada
    return sorted_list