list_group = ["IDF2101", "IDF2102", "IDF2103", "IDF2104", "IDF2105", 
                  "IDF2201", "IDF2202", "IDF2203", "IDF2204", "IDF2205", 
                  "IDF2301", "IDF2302", "IDF2303", "IDF2304", "IDF2305", 
                  "IDF2401", "IDF2402", "IDF2403", "IDF2404", "IDF2405"]

def key_function(item):
    # La clave es el número que aparece en el medio de cada cadena
    return int(item[3:7])

# Ordena la lista utilizando la función de clave personalizada
sorted_list = sorted(list_group, key=key_function)

# Imprime la lista ordenada
print(sorted_list)