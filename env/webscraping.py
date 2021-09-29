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
print(times)

#estatisticas
html_estatisticas = soup.find_all(attrs={'class': "classificacao__pontos"})
estatisticas = []
for estatistica in html_estatisticas:
  estatisticas.append(estatistica.get_text())
array_estatisticas = np.array_split(estatisticas, 20)
estatisticas.clear()
for array in array_estatisticas:
  estatisticas.append(list(array))
print(estatisticas)



 #estruturando conteudo em um Dat Frame- Pandas


driver.close()




