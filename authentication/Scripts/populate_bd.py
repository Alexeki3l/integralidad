from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from integralidad.authentication.models import Profile

import pandas as pd

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "integralidad.settings")

def populate_bd_with_excel_file():
    try:    
        df = pd.read_excel('./user_random.xlsx')

        for index, row in df.iterrows():
            print(index, row)
            # user_object = User(
            #     password =,
            #     username =,
            #     first_name =,
            #     last_name =,
            #     email =,
            # )
            # print(row)
            break
    
    except:
        pass
    
populate_bd_with_excel_file()