import requests
from bs4 import BeautifulSoup

def get_mamodo_list_links():
    url = 'https://zatchbell.fandom.com/wiki/Mamodos_and_Bookkeepers'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    mamodo_soup = soup.select('#toc li a .toctext')
    
    mamodo_soup_list = []
    mamodo_list = []

    for mamodo in mamodo_soup:
        mamodo_soup_list.append(mamodo.get_text())

    for mamodo in mamodo_soup_list:
        mamodo = mamodo.replace(" ","_")
        mamodo = 'https://zatchbell.fandom.com/wiki/'+mamodo
        mamodo_list.append(mamodo)
        
    with open('mamodo_list_final.txt', 'w', encoding="utf-8") as file:
        file.write("\n".join(mamodo_list) + "\n")
  

def get_mamodo_link_in_list():
    mamodo_id = 0
    with open('mamodo_list_final.txt', 'r', encoding="utf-8") as file:
        #for mamodo in file:
        mamodo = file.readline()
        mamodo_id += 1
        get_mamodo_informations(mamodo_id, mamodo.strip())


def get_mamodo_informations(mamodo_id, mamodo):

    #Remover parte do link para ter o Id do nome da dupla
    id_dupla = mamodo.replace('https://zatchbell.fandom.com/wiki/',"")

    response = requests.get(mamodo)
    soup = BeautifulSoup(response.content, 'html.parser')

    dupla_nome = soup.select('#'+id_dupla )
    spells = soup.select('Spells table')
    print(dupla_nome)
    print(spells)

    with open('mamodo.html', 'w', encoding="utf-8") as file:
        file.write(repr(soup))

def get_spell_informations():
    pass

#get_mamodo_list_links()
#get_mamodo_informations()

get_mamodo_link_in_list()