import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units

'''plotando t e td em um diagrama skewT '''

#abrindo a planilha de dados
df = pd.read_csv("/home/joao/meteorologia/radiossondagem_atv_meteorologia.csv")
print(df)

#excluindo colunas sem dados de T e Td (-999)
#df = df.dropna(subset=('Pres[hPa]', 'Geop[m]', 'Temp[oC]', 'Td[oC]','Dir[o]','Vel[m/s]'
                       #), how='all').reset_index(drop=True)
df.drop(df[df['Temp[oC]'] == -999].index, inplace = True)
df.drop(df[df['Td[oC]'] == -999].index, inplace = True)

#definindo as variaveis separadamente
pressao=df['Pres[hPa]']
geop=df['Geop[m]']
T=df['Temp[oC]']
Td=df['Td[oC]']
Dir=df['Dir[o]']
Vel=df['Vel[m/s]']
#u,v=mpcalc.wind_components(Vel,Dir)

#plotando 
skew=SkewT()
skew.plot(pressao, T, 'r')
skew.plot(pressao, Td, 'g')
skew.ax.set_xlabel('Temperatura (\N{DEGREE CELSIUS})')
skew.ax.set_ylabel('Pressão (hPa)')

# Adicionando as linhas
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
skew.ax.set_ylim(1000, 100)

#adicionando ncl
lcl_pressure, lcl_temperature = mpcalc.lcl(pressao[0]*units.mbar, T[0]*units.degC, Td[0]*units.degC)
skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
plt.show()
exit()
# Calculate full parcel profile and add to plot as black line
prof = mpcalc.parcel_profile(pressao*units.mbar, T*units.degC, Td*units.degC)
skew.plot(pressao*units.mbar, prof*units.degC, 'k', linewidth=2, label='SB PARCEL PATH')
plt.show()
exit()

# Shade areas of CAPE and CIN
skew.shade_cin(pressao, T, prof, Td, alpha=0.2, label='SBCIN')
skew.shade_cape(pressao, T, prof, alpha=0.2, label='SBCAPE')
plt.legend()
plt.show()

#fonte =https://unidata.github.io/MetPy/latest/examples/plots/Simple_Sounding.html#sphx-glr-examples-plots-simple-sounding-py

#fonte2 =https://github.com/Unidata/MetPy/issues/2460
