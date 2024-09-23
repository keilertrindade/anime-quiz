import json
import re
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
        for mamodo in file:
            mamodo_id += 1
            get_mamodo_informations(mamodo_id, mamodo.strip())
            #extract_duo_data(mamodo.strip())


def get_mamodo_informations(mamodo_id, mamodo):

    #Remover parte do link para ter o Id do nome da dupla
    #id_dupla = mamodo.replace('https://zatchbell.fandom.com/wiki/',"")

    response = requests.get(mamodo)
    tree = html.fromstring(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    duo_name = extract_text(tree.xpath('//*[@id="firstHeading"]/span'))
    color_book = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[1]/b'))
    if color_book is None:
        color_book = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[1]/b'))
    if color_book is None:
        color_book = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/b'))

    gender_human = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[3]'))
    gender_mamodo = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/div/div/table/tbody/tr[3]/td[2]'))
    spell_main_type = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[6]/td/table[1]/tbody/tr/td[2]/b'))
    spell_secondary_type = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[6]/td/table[2]/tbody/tr/td[2]/b'))
    ethics = extract_text(tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[3]/td/div/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/b'))

    spells = soup.select("[style*='text-align:center;border:2px solid black;color:black; -moz-border-radius:7px;border-radius:7px;background-color:gray;color:white']")
    spell_1 = tree.xpath('//*[@id="mw-content-text"]/div/table[3]')

    duo_data = {
    "duo_name": duo_name,
    "color_book": color_book,
    "gender_human": gender_human,
    "gender_mamodo": gender_mamodo,
    "spell_main_type": spell_main_type,
    "spell_secondary_type": spell_secondary_type,
    "ethics": ethics
}
    json_data = json.dumps(duo_data)
    print(json_data)

    #for spell in spells:
    #    extract_spell_data(spell)
        #print(spell)
    #    print("--------------------------------------------------------------")

def extract_spell_data(soup_element):
    # Extrair o nome do feitiço
    spell_name = soup_element.find('a').text.strip()

    # Extrair o nome em japonês e remover caracteres não latinos (kanji, etc.)
    japanese_name_text = soup_element.find(string="Japanese Name:").parent
    japanese_name = japanese_name_text.next_sibling.strip()

    # Remover qualquer caractere japonês usando uma regex que elimina caracteres fora do alfabeto latino
    japanese_name_cleaned = re.sub(r'[^\x00-\x7F]+', '', japanese_name)
    japanese_name_cleaned = japanese_name_cleaned.replace('(','')
    japanese_name_cleaned = japanese_name_cleaned.replace(')','')
    japanese_name_cleaned = japanese_name_cleaned.strip()


    # Extrair o tipo de feitiço
    spell_type_text = soup_element.find(string="Type(s):").parent
    spell_type = spell_type_text.next_sibling.strip()

    # Extrair o poder principal e secundário (opcional)
    #main_spell_power = soup_element.find('td', style="color:yellow;text-align:left;").text.strip()
    #secondary_spell_power = soup_element.find('td', style="color:#FF6666;text-align:left;").text.strip() if soup_element.find('td', style="color:#FF6666;text-align:left;") else "None"

    # Extrair a descrição do feitiço
    spell_description_text = soup_element.find(string="Description:").parent
    spell_description = spell_description_text.next_sibling.strip()

    # Construir o dicionário com os dados extraídos
    spell_data = {
        "duo_id": "to_be_filled",  # Preencher com o identificador único apropriado
        "japanese_name": japanese_name_cleaned,  # Nome japonês sem caracteres japoneses
        "english_name": spell_name,
        "main_spell_power": 'main_spell_power',
        "secondary_spell_power": 'secondary_spell_power',
        "spell_type": spell_type,
        "spell_description": spell_description
    }

    # Converte o dicionário para uma string JSON formatada
    json_output = json.dumps(spell_data, indent=4)
    print(json_output)

# Exemplo de uso com um elemento BeautifulSoup já processado
# Supondo que 'soup_element' seja o objeto do tipo <class 'bs4.element.Tag'> que você já processou
# extract_spell_data(soup_element)


def extract_text(element_list):
    if element_list and len(element_list) > 0:
        return element_list[0].text_content().strip()  # Usa text_content() para extrair o texto
    return None


def extract_duo_data(url):
    # Fazer a requisição à página do link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Procurar todas as tabelas com bordas (ou outro critério)
    tables = soup.find_all('table', {'style': lambda x: x and 'border' in x})

    if not tables:
        print(f"Nenhuma tabela encontrada em {url}")
        return None

    # Dicionário para armazenar os dados do duo
    duo_data = {
        'duo_name': "N/A",
        'color_book': "N/A",
        'gender_human': "N/A",
        'gender_mamodo': "N/A",
        'spell_main_type': "N/A",
        'spell_secondary_type': None,
        'ethics': "N/A"
    }

    for table in tables:
        rows = table.find_all('tr')

        # Primeiro tentamos obter os nomes da dupla
        try:
            mamodo_name = rows[1].find_all('td')[0].text.strip()
            partner_name = rows[1].find_all('td')[1].text.strip()
            duo_data['duo_name'] = f"{mamodo_name} and {partner_name}"
        except IndexError:
            pass  # Se não conseguir, seguimos para tentar o resto

        # Iteramos pelas linhas para capturar os campos corretos
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:  # Precisamos de 2 células para chave-valor
                header = cells[0].text.strip().lower()
                value = cells[1].text.strip()

                # Mapeamos as informações corretamente
                if 'book' in header:
                    duo_data['color_book'] = value
                elif 'gender' in header and 'mamodo' in header:
                    duo_data['gender_mamodo'] = value
                elif 'gender' in header and 'partner' in header:
                    duo_data['gender_human'] = value
                elif 'spell' in header and 'main' in header:
                    duo_data['spell_main_type'] = value
                elif 'spell' in header and 'secondary' in header:
                    duo_data['spell_secondary_type'] = value if value else None
                elif 'ethics' in header:
                    duo_data['ethics'] = value


    #return duo_data
    print(duo_data)

def get_spell_informations():
    pass

#get_mamodo_list_links()
#get_mamodo_informations()

get_mamodo_link_in_list()