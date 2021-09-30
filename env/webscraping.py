import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import json
import numpy as np

url = "https://ge.globo.com/futebol/brasileirao-serie-a/"


option = Options()

option.add_argument("--headless")

driver = wd.Chrome(options=option)

driver.get(url)

time.sleep(5)

elemento = driver.find_element_by_class_name('classificacao__pontos-corridos')

html__do_elemento = elemento.get_attribute("outerHTML")

# Utilizando o BeaultifulSoup
soup = BeautifulSoup(html__do_elemento, 'html.parser')

#times
html_times = soup.find_all(attrs= {"class": "classificacao__equipes classificacao__equipes--sigla"})
times = []
for time in html_times:
  times.append(time.get_text())


#estatisticas
html_estatisticas = soup.find_all(attrs={'class': "classificacao__pontos"})
estatisticas = []
for estatistica in html_estatisticas:
  estatisticas.append(estatistica.get_text())
array_estatisticas = np.array_split(estatisticas, 20)
estatisticas.clear()
for array in array_estatisticas:
  estatisticas.append(list(array))
#Acessando o site da ESPN

url_espn = "https://www.espn.com.br/futebol/estatisticas/_/liga/bra.1"

driver.get(url_espn)

#Pegando os dados da tabela artilharia

tabela_artilharia = driver.find_element_by_class_name('Table__TBODY')

tabela_artilharia_html = tabela_artilharia.get_attribute('outerHTML')

soup2 = BeautifulSoup(tabela_artilharia_html, 'html.parser')

artilheiros = soup2.find_all(attrs={"class":"tar Table__TD"})
dicionario_artilheiros = dict()
#Pegando os nomes dos artilheiros
nomes_dos_artilheiros = list()
for i in range(1,60,5):
  nomes_dos_artilheiros.append(soup2.find_all(attrs={"class":"Table__TD"})[i].a.get_text())
dicionario_artilheiros["Nome do Artilheiro"] = nomes_dos_artilheiros
#pegando os times dos artilheiros
times_dos_artilheiros = list()
for i in range(2,48,5):
  try:
    times_dos_artilheiros.append(soup2.find_all(attrs={"class":"Table__TD"})[i].a.get_text())
  except AttributeError:
    times_dos_artilheiros.append(("Sem time"))
dicionario_artilheiros["Time dos artilheiros"] = times_dos_artilheiros
#pegando os gols feitos pelo top 10 artilheiros
qtd_gols_artilheiro = list()
for i in range(1, 21, 2):
  qtd_gols_artilheiro.append(soup2.find_all(attrs={"class":"tar Table__TD"}[i].span.get_text()))
dicionario_artilheiros["qtd gols por artilheiro"] = qtd_gols_artilheiro


print(dicionario_artilheiros)



 #estruturando conteudo em um Dat Frame- Pandas


driver.close()




