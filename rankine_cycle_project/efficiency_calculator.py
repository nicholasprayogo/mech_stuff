import pandas as pd
import numpy as np

data = pd.read_csv('steam_data.tsv', sep='\t')
data = data.rename(columns={'Temperature (C)':'temperature',
                    'Pressure (bar)':'pressure',
                    'Enthalpy (v, kJ/kg)':'enthalpy_g',
                    'Enthalpy (l, kJ/kg)':'enthalpy_f',
                    'Entropy (v, J/g*K)': 'entropy_g',
                    'Entropy (l, J/g*K)': 'entropy_f'})

print(data['pressure'])
print(data.columns)
