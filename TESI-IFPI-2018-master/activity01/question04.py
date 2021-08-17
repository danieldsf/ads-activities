from libs.myurllib import get_parsed
from time import sleep

base_url = 'http://example.webscraping.com'

for i in range(1,25):
    sleep(1)
    
    soup = get_parsed('%s/places/default/index/%s' % (base_url, i), True)

    url = [row['href'] for row in soup.find('div', id='results').find_all('a')]
    
    for url in urls:
        try:
            soup = get_parsed('%s%s'% (base_url, url))
            name = soup.find(attrs={'id':'places_country__row'}).find(attrs={'class':'w2p_fw'}).get_text()
            population = soup.find(attrs={'id':'places_population__row'}).find(attrs={'class':'w2p_fw'}).get_text()
            area = soup.find(attrs={'id':'places_area__row'}).find(attrs={'class':'w2p_fw'}).get_text().replace(' square kilometres','')

            population = int(population.replace(',',''))
            area = int(area.replace(',',''))
            print('nome do pais: %s | populacao: %s hab | area: %s km2 | densidade demografica : %.2f hab/km2\n' % (name,population,area))
            sleep(1)
        except expression as identifier:
            print('Erro ao buscar dados')
        

        