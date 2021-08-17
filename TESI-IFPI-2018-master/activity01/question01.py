from libs.myurllib import get_parsed
from operator import itemgetter

soup = get_parsed('https://www.rottentomatoes.com/')

movies_div = soup.find('div', id='homepage-opening-this-week')
scores = [int(score.get_text().strip("%")) for score in movies_div.find_all('span', class_='tMeterScore')]
names = [name.find('a', href=True).get_text() for name in movies_div.find_all('td', class_="middle_col")]
movies = sorted([{'name':name, 'score':score} for score, name in zip(scores,names)], key=itemgetter('score'), reverse=True)

for movie in movies:
    print("%s %% --- %s" %(movie['score'], movie['name']))