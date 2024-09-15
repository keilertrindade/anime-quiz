import requests
from bs4 import BeautifulSoup

url = 'https://zatchbell.fandom.com/wiki/Mamodos_and_Bookkeepers'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
#mamodo_soup = soup.find_all("li","toclevel-1")
mamodo_soup = soup.select('#toc li a .toctext')

mamodo_list = []
mamodo_soup_list = []

for mamodo in mamodo_soup:
    #mamodo_list.append(mamodo)
    mamodo_soup_list.append(mamodo.get_text())

#print(mamodo_list)

for mamodo in mamodo_soup_list:
    mamodo = mamodo.replace(" ","_")
    mamodo = 'https://zatchbell.fandom.com/wiki/'+mamodo
    mamodo_list.append(mamodo)
    
with open('mamodo_list_final.txt', 'w', encoding="utf-8") as file:
   file.write(repr(mamodo_list))
