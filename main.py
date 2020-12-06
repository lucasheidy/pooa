#Universidade Federal de São Carlos
#Departamento de Computação
#Professor Daniel Lucrédio
#Alunos:
#       Lucas Heidy Tuguimoto Garcia 743565
#       Roger Sigolo Junior 728340
#Programação Orientada a Objetos Avançada
#Trabalho 2


#Neste trabalho introduzimos uma ferramenta para encontrar notícias dos principais sites e seus respectivos links. Ainda, é intuito do trabalho praticar e seguir o príncipios Fechado-Aberto e de Responsabilidade Única, do acrônimo SOLID. 

#Para tanto, as seguintes extensões foram providas para serem levadas em conta ao pensar nos príncipios:
#Extensão 1: Deve ser possível incluir novos sites de notícias (ex: UOL, Estadão, etc)
#Extensão 2: Deve ser possível incluir novos algoritmos, além de salvar em .csv (ex: imprimir na tela, baixar os conteúdos das notícias, seguindo os links, criar uma nuvem de palavras com todos os títulos de notícias do dia, aplicar um algoritmo de aprendizado de máquina para detectar tendências e diferenças entre os sites, sei lá)


import urllib3
from bs4 import BeautifulSoup
import csv
from abc import ABC, abstractmethod

#website é uma classe abstrata que serve para g1 e uol herdarem os atributos link e classe, e o método to_list

class website(ABC):
  def __init__(self,link, classe):
   self.link = link
   self.classe = classe
  @abstractmethod
  def to_list(self, collection):
    return 0

#g1 e uol são os dois primeiros sites adicionados e é possível adicionar um novo, para isso é necessário criar uma classe que herde de website e então dar override na função to_list. Isso porque o html dos sites não é padronizado.    

#Por exemplo, em g1, para pegar o titulo basta dar strip(retirar apenas o texto fora de tags) na sessão de html encontrada e pegar o conteudo de href= dentro da mesma tag.
class g1(website):
  def to_list(self, collection):
    lista = []
    for news in collection:
      aux = []
      aux.append(news.text.strip())
      aux.append(news['href'])
      lista.append(aux)

    return lista

#Já no uol, na mesma tag de html temos o link da noticia principal, mas no texto temos várias noticias recomendadas. Além disso, href com o link da noitica está numa tag mais externa em relação ao titulo, o que é o contrário do G1, portanto a busca também é diferente.
#Por esses motivos, a extensão para adicionar novos sites requer que sejam feitas classes novas, já que a função to_list de cada site é diferente.

class uol(website):
  def to_list(self, collection):
    title = []
    link = []
    lista = []

    for news in collection:
      headline = news.text.strip()
      aux = headline.split("      ")
      title = title + aux 

      for div in news.find_all('a'):
        href = div.get('href')
        link.append(href)

    for i in range(len(title)):
      aux = []
      aux.append(title[i])
      aux.append(link[i])
      lista.append(aux)

    return lista  


#A classe 'htmlGetter' é responsável por instanciar um pool manager, e requisitar o html do site requerido
#Obs: apesar, de deliberadamente citarmos mais de uma responsabilidade à classe, só há um motivo para mudar a classe, que está relacionado a forma de obter o html usando urllib3

class htmlGetter:
  manager = urllib3.PoolManager()

  def requestHTML(self, website):
    html = self.manager.request('GET', website.link)
    return html

#a classe soupMaker passa o html para o Parser BeautifulSoup.
class soupMaker:
  def make_soup(self, html):
    return BeautifulSoup(html.data, 'html.parser')

#A classe 'newsFinder' acha todas as tags contendo a classe espefica do site onde estão as informações necessárias (titulo, link). 
class newsFinder: 
  
  def findAll(self, website, soup):
    return soup.find_all(class_= website.classe)


#A classe 'newWriter' é responsável pela escrita dos elementos de uma 'list' em um arquivo csv. Neste projeto, a utilizamos para escrever os títulos e links das notícias dos principais sites, passando uma lista contendo o resultado encontrado no html dos sites respectivos.
#Se for necessário adicionar um novo atributo a ser buscado no site, não seria necessário reescrever o código desta classe, pois "writerows" escreve uma tupla, separada por elemento, no arquivo csv, se a tupla tivesse dimensão maior este código continua funcionando.
class newsWriter:

  def to_write(self, lista):
    with open('news.csv', 'a') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerows(lista)

#MAIN
#Neste projeto realizamos uma busca no html dos websites 'g1.globo.com' e 'uol.com.br', selecionamos títulos de notícias e seus respectivos links, e os escrevemos em arquivo '.csv'.

#Se algum dia a classe onde o texto do titulo mudar ou a globo perder o domínio, então é só criar o objeto g1 com a classe(html) de dominio diferente. Assim não é necessário mudar a classe g1 (nem a uol se o mesmo acontecer)

wg1 = g1("https://g1.globo.com/", "feed-post-link gui-color-primary gui-color-hover")

hg = htmlGetter()
nf = newsFinder()
nw = newsWriter()
sm = soupMaker()

html = hg.requestHTML(wg1)
soup = sm.make_soup(html)
collection = nf.findAll(wg1, soup)
lista = wg1.to_list(collection)
nw.to_write(lista)

wuol = uol("www.uol.com.br/", "submanchete submanchete-destaque submanchete-ultimo has-image")

html2 = hg.requestHTML(wuol)
soup2 = sm.make_soup(html2)
collection2 = nf.findAll(wuol, soup2)
lista2 = wuol.to_list(collection2)
nw.to_write(lista2)

#Para extender o código com a finalidade de implementar uma funcionalidade diferente, incluindo um novo algoritmo, não é necessário reescrever código. Isto se deve ao fato de ser possível alimentar o novo algoritmo através da lista gerada pelo método "to_list" de cada classe referente à um site específico. 