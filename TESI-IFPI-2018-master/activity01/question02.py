from libs.myurllib import get_parsed

soup = get_parsed('https://www.imdb.com/chart/boxoffice')

movies_div = soup.find('table', class_='chart full-width')

values = [float(movie.get_text().replace(' ','').replace('\n','').replace('$','').replace('M','')) for movie in movies_div.find_all('td', 'ratingColumn')]
weekends = values[0::2]
grosses = values[1::2]
names = [movie.get_text().replace('\n','').replace(' ','') for movie in movies_div.find_all('a', href=True) if movie.get_text().replace('\n','').replace(' ','')!='']
weeks = [int(week.get_text()) for week in movies_div.find_all('td',class_='weeksColumn')]
movies = sorted([{'name':name, 'weekend':weekend, 'gross':gross, 'week':week } for name, weekend, gross, week in zip(names,weekends,grosses,weeks)], key=itemgetter('weekend'), reverse=True)

print('weeks | weekend (US$ Mi)| gross (US$ Mi) | name')
print('-----------------------------------------------')
for movie in movies:	
    print("%s%s| %s%s| %s%s | %s"%(movie['week'],(6-len(str(movie['week'])))*' ',movie['weekend'],(16-len(str(movie['weekend'])