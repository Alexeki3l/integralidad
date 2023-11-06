from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Profile

import pandas as pd
import os

def populate_bd_with_excel_file():
    try:
        if User.objects.all().count() < 5:
            try:
                ruta_actual = os.path.abspath(__file__)
                ruta_raiz = str(ruta_actual)[:-8]
                # print(ruta_actual)
                ruta_file = f"{ruta_raiz}Scripts/user_random.xlsx"
                df = pd.read_excel(ruta_file)

                users_to_create = []
                profiles_to_create = []

                excel_data = df.iterrows()
                
                for index, row in excel_data:
                    print(index, row)
                    # break
                    rol_facultad = ['','estudiante', 'profesor guia', 'profesor de año', 'vicedecana/o']
                    rol_universidad = ['','estudiante', 'profesor', 'vicedecana/o']
                    try:
                        user_object = User.objects.create_user(
                            password=row['contraseña'],
                            username=row['usuario'],
                            first_name=row['nombre'],
                            last_name=row['apellidos'],
                            email=row['correo'],
                        )
                        # user_object.set_password(row['contraseña'])
                        # user_object.save()
                    except:
                        continue
                    
                    if str(row['año']) == 'Nan':
                        year = 0
                    else:
                        year = int(row['año'])
                    
                    # users_to_create.append(user_object)
                    defaults={
                        'rol_fac':rol_facultad.index(row['rol_facultad']),
                        'rol_universitario':rol_universidad.index(row['rol_universitario']),
                        'solapin':str(row['solapin']),
                        'grupo':str(row['grupo']),
                        'carrera':row['carrera'],
                        'provincia':row['provincia'],
                        'municipio':row['municipio'],
                        'ci':str(row['carnet_identidad']),
                        'id_exp':str(row['id_expediente']),
                        'academy_year':year,
                    }

                    objeto, creado = Profile.objects.update_or_create(
                        user                =user_object,
                        # rol_fac             =rol_facultad.index(row['rol_facultad']),
                        # rol_universitario   =rol_universidad.index(row['rol_universitario']),
                        # solapin             =str(row['solapin']),
                        # grupo               =str(row['grupo']),
                        # carrera             =row['carrera'],
                        # provincia           =row['provincia'],
                        # municipio           =row['municipio'],
                        # ci                  =str(row['carnet_identidad']),
                        # id_exp              =str(row['id_expediente']),
                        # academy_year        =int(row['año']),
                        defaults=defaults
                    )
                    # profiles_to_create.append(profile)

                # Profile.objects.bulk_create(profiles_to_create)

                print('Datos Cargados')

            except FileNotFoundError as e:
                print('ERROR: ', e)
                
            except Exception as e:
                print(e)
    except:
        pass
