import pandas as pd
import matplotlib.pyplot as plt
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
df = df[(df['Temp[oC]'] != -999) & (df['Td[oC]'] != -999)]

#definindo as variaveis separadamente e adicionando as unidades
pressao = df['Pres[hPa]'].values * units.hPa
T = df['Temp[oC]'].values * units.degC
Td = df['Td[oC]'].values * units.degC


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
lcl_pressure, lcl_temperature = mpcalc.lcl(pressao[0], T[0], Td[0])
skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')
# Calculate full parcel profile and add to plot as black line
prof = mpcalc.parcel_profile(pressao, T, Td)
skew.plot(pressao*units.mbar, prof*units.degC, 'k', linewidth=2, label='SB PARCEL PATH')

# Shade areas of CAPE and CIN
skew.shade_cin(pressao, T, prof, Td, alpha=0.2, label='SBCIN')
skew.shade_cape(pressao, T, prof, alpha=0.2, label='SBCAPE')
plt.show()

#fonte =https://unidata.github.io/MetPy/latest/examples/plots/Simple_Sounding.html#sphx-glr-examples-plots-simple-sounding-py

#fonte2 =https://github.com/Unidata/MetPy/issues/2460
