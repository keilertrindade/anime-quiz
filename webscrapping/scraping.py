import requests
from lxml import html
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
    tree = html.fromstring(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    nome_dupla = tree.xpath('//*[@id="firstHeading"]/span')
    color_book = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[1]/b')
    #age_human = tree.xpath('')
    #age_mamodo = tree.xpath('')
    gender_human = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]')
    gender_mamodo = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[2]')
    spell_main_type = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[6]/td/table[1]/tbody/tr/td[2]/b')
    spell_secondary_type = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[6]/td/table[2]/tbody/tr/td[2]/b')
    ethics = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/b')

    spells = soup.select("[style*='text-align:center;border:2px solid black;color:black; -moz-border-radius:7px;border-radius:7px;background-color:gray;color:white']")
    spell_1 = tree.xpath('//*[@id="mw-content-text"]/div/table[3]')

    for spell in spells:
        print(spell)
        print("--------------------------------------------------------------")

    #print(ethics[0].text)


def get_spell_informations():
    pass

#get_mamodo_list_links()
#get_mamodo_informations()

get_mamodo_link_in_list()