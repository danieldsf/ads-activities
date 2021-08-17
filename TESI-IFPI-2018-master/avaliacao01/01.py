import requests_cache, requests
import re
from bs4 import BeautifulSoup as bs
from operator import itemgetter
from time import sleep


requests_cache.install_cache()

def download(url, quiet=False, num_retries=2):
	if not quiet:
		print('Downloading data from:', url)
	page = None
	try:
		response = requests.get(url)
		page = response.text
		if response.status_code >= 400:
			print('Download error:', response.text)
		if num_retries and 500 <= response.status_code < 600:
			return download(url, num_retries - 1)
	except requests.exceptions.RequestException as e:
		print('Download error:', e.reason)
	return page

def hora_do_show(elemento):
	page = download(elemento['href'])
	soup = bs(page, 'html.parser')

	print(soup.find(attrs={'class':'post_content'}).get_text())
	input("pressione para continuar... ")

base_url = 'http://www.tce.pi.gov.br'
page = download(base_url)

### (2,0) Baixe o título das 5 notícias da página inicial;

soup = bs(page, 'html.parser')
results = [news.find('a') for news in soup.find(attrs={'class':'latestnews'})]
titulos = list(set(results))

op = "0"
while op!="6":
	for i in range(5):
		print ("%s - %s" %(i+1, titulos[i].get_text()))
	print("6 - sair")
	op = input("---> ")
	if(op != "6" and int(op) > 0 and int(op) < 7):
		hora_do_show(titulos[int(op)-1])


'''

•
•
•
•
(2,0) Baixe o título das 5 notícias da página inicial;
(0,5) Forneça uma opção um menu com escolha de 1 a 6
correspondendo às 5 matérias e uma sexta opção de sair;
(2,0) Caso o usuário escolha uma das opções, o texto da
mensagem deve ser baixado e exibido.
(0,5) Após exibir a matéria, deve-se da a opção para exibir o
menu novamente.
Nota: necessariamente use a biblioteca requests-cache para
evitar requisições desnecessárias

'''

'''
for i in range(1,26):
	print('\n   BAIXANDO CONTEUDO DA PAGINA ',i, '\n')
	sleep(0.75)
	soup = bs(download(base_url+'/places/default/index/'+str(i)+'/', quiet=True), 'html.parser')
	countries_urls = [row['href'] for row in soup.find('div', id='results').find_all('a')]
	for coutry_url in countries_urls:	
		country_soup = bs(download(base_url+coutry_url, quiet=True), 'html.parser')
		country_name = country_soup.find(attrs={'id':'places_country__row'}).find(attrs={'class':'w2p_fw'}).get_text()
		country_population = country_soup.find(attrs={'id':'places_population__row'}).find(attrs={'class':'w2p_fw'}).get_text()
		country_area = country_soup.find(attrs={'id':'places_area__row'}).find(attrs={'class':'w2p_fw'}).get_text().replace(' square kilometres','')
		print('nome do pais: %s | populacao: %s hab | area: %s km2 | densidade demografica : %.2f hab/km2\n' %(country_name,country_population,country_area,   int(country_population.replace(',',''))/int(country_area.replace(',',''))))
		sleep(0.5)
'''