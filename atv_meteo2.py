import pandas as pd
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.units import units
from metpy.plots import SkewT

# Abrindo a planilha de dados
df = pd.read_csv("/home/joao/meteorologia/radiossondagem_atv_meteorologia.csv")

# Excluindo linhas em que 'Temp[oC]' ou 'Td[oC]' é igual a -999
df = df[(df['Temp[oC]'] != -999) & (df['Td[oC]'] != -999)]
df = df.reset_index(drop=True)

# Definindo as variáveis separadamente e adicionando as unidades - unidades são fundamentais para o funcionamento correto!
pressao = df['Pres[hPa]'].values * units.hPa
T = df['Temp[oC]'].values * units.degC
Td = df['Td[oC]'].values * units.degC

# Plotando
skew = SkewT()

# Adicionando as linhas
skew.plot(pressao, T, 'r', label='T')
skew.plot(pressao, Td, 'g', label='Td')
#adiabatica seca
skew.plot_dry_adiabats()
#pseudoadiabatica ou adiabatica umida
skew.plot_moist_adiabats()
#linhas de razao de mistura
skew.plot_mixing_lines()

# Adicionando NCL
lcl_pressure, lcl_temperature = mpcalc.lcl(pressao[0], T[0], Td[0])
skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black', label='NCL')

#Adicionando perfil da parcela -> a parecela segue uma pseudoadiabatica depois do NCL
prof = mpcalc.parcel_profile(pressao, T[0], Td[0])
skew.plot(pressao, prof, 'k',linestyle='--', linewidth=2, label='Perfil da parcela')
# Adicionando NE 
el_pressure,el_temperature=mpcalc.el(pressao, T, Td, prof)
skew.plot(el_pressure,el_temperature,'ko',markerfacecolor='red',label='NE')
#Adicionando NCE
lfc_pressure,lfc_temperature=mpcalc.lfc(pressao, T, Td)
skew.plot(lfc_pressure,lfc_temperature,'ko',markerfacecolor='blue',label='NCE')

# Sombreando área de CAPE 
skew.shade_cape(pressao, T, prof,color='c', label='CAPE')
#Adicionando área de CINE
skew.shade_cin(pressao, T, prof, Td,color='r', label='CINE')

# Definindo rótulos e legenda
plt.xlabel('Temperatura (°C)')
plt.ylabel('Pressão (hPa)')
plt.legend()

# Mostrando o diagrama de Skew-T
plt.show()
