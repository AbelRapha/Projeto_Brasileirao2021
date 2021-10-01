import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import json

url = "https://www.espn.com.br/futebol/liga/_/nome/bra.1/brasileiro"


option = Options()

option.add_argument("--headless")

driver = wd.Chrome(options=option)

driver.get(url)

time.sleep(5)

elemento = driver.find_element_by_class_name('content')

html__da_tabela= elemento.get_attribute("outerHTML")

# Utilizando o BeaultifulSoup
soup = BeautifulSoup(html__da_tabela, 'html.parser')

dicionario_campeonato = dict()
#times
tabela_campeonato = soup.find_all(attrs={"class": "mod-data"})
tabela_campeonato= tabela_campeonato[0]
times = tabela_campeonato.find_all("tr")
lista_times = list()
for i in range(1,len(times),1):
  lista_times.append(times[i].a.get_text())
dicionario_campeonato['Times'] =  lista_times
#Quantidade de Pontos:
qtd_pts = list()
tabela_campeonato = soup.find_all(attrs={"class": "mod-data"})
tabela_campeonato= tabela_campeonato[0].find_all(attrs = {"class": "right"})
for i in range(11,126,6):
  qtd_pts.append(tabela_campeonato[i].get_text())
dicionario_campeonato['QTD Pontos'] = qtd_pts

#Quantidade de Jogos:
qtd_jogos = list()
for i in range(6,126,6):
  qtd_jogos.append(tabela_campeonato[i].get_text())
dicionario_campeonato['QTD Jogos'] =  qtd_jogos

#Quantidade de Vitorias
qtd_vitorias = list()
for i in range(7,126,6):
  qtd_vitorias.append(tabela_campeonato[i].get_text())
dicionario_campeonato['QTD Vitorias'] = qtd_vitorias

#Quantidade de empates
qtd_empates = list()
for i in range(8,126,6):
  qtd_empates.append(tabela_campeonato[i].get_text())
dicionario_campeonato['QTD Empates'] =  qtd_empates

#Quantidade Derrotas
qtd_derrotas = list()
for i in range(9,126,6):
  qtd_derrotas.append(tabela_campeonato[i].get_text())
dicionario_campeonato['QTD Derrotas'] =  qtd_derrotas

#Saldo de Gols:
qtd_sg = list()
for i in range(10,126,6):
  qtd_sg.append(tabela_campeonato[i].get_text())
dicionario_campeonato['SALDO DE GOLS'] = qtd_sg


#Acessando o site da ESPN Seção de estatísticas

url_espn = "https://www.espn.com.br/futebol/estatisticas/_/liga/bra.1"

driver.get(url_espn)

#Pegando os dados da tabela artilharia

tabela_artilharia = driver.find_element_by_class_name('Table__TBODY')

tabela_artilharia_html = tabela_artilharia.get_attribute('outerHTML')

soup2 = BeautifulSoup(tabela_artilharia_html, 'html.parser')

artilheiros = soup2.find_all(attrs={"class":"tar Table__TD"})

#Pegando os nomes dos artilheiros
nomes_dos_campeonato = list()
for i in range(1,60,5):
  nomes_dos_campeonato.append(soup2.find_all(attrs={"class":"Table__TD"})[i].a.get_text())
dicionario_campeonato["Nome do Artilheiro"] = nomes_dos_campeonato
#pegando os times dos artilheiros
times_dos_campeonato = list()
for i in range(2,48,5):
  try:
    times_dos_campeonato.append(soup2.find_all(attrs={"class":"Table__TD"})[i].a.get_text())
  except AttributeError:
    times_dos_campeonato.append(("Sem time"))
dicionario_campeonato["Time dos campeonato"] = times_dos_campeonato
#pegando os nomes dos garcons(jogadores com mais assistências)
tabela_assistencias_html = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[3]/div/div/section/div/section/div/div[2]/section/div/div[2]/div/div[2]/table')

soup4 = BeautifulSoup(tabela_assistencias_html, 'html.parser')

tabela_assistencias = soup4.find_all(attrs={"class": "Table__TR Table__TR--sm Table__even"})
#Nomes
nomes_garcons = list()
for i in range(0,10,1):
  nomes_garcons.append(tabela_assistencias[i].a.get_text())
dicionario_campeonato['Nome Jogador Assistência'] =  nomes_garcons
#Times respectivos
times_garcons = soup4.find_all("a")
times_garcons_lista = list()
for i in range(1,21,2):
  times_garcons_lista.append(times_garcons[i].get_text())
dicionario_campeonato['Times dos jogadores com mais assistência'] = times_garcons_lista

print(dicionario_campeonato)



 #estruturando conteudo em um Data Frame- Pandas


driver.close()




