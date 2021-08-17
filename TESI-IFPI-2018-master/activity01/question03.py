from libs.myurllib import get_parsed, session, Moment, easy_get_text

soup = get_parsed('https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi')

#

temperature = easy_get_text(soup, 'p','left normal txt-gray-cw temp-topo', True)
condition = easy_get_text(soup, 'p', 'momento-condicao')
sensation = easy_get_text(soup, 'li', 'momento-sensacao')
humidity = easy_get_text(soup, 'li', 'momento-humidade')
pressure = easy_get_text(soup, 'li', 'momento-pressao')
wind = easy_get_text(soup, 'a', 'momento-vento').replace(' ','').replace('\n','').replace('\xa0','')
update = easy_get_text(soup, 'p', 'momento-atualizacao').replace('\n','').replace(' ','').replace('Atualizadoàs','')

# 

m = Moment(temperature, condition, sensation, humidity, pressure, wind, update)

has_same = len(session.query(Moment)
    .filter(Moment.update == m.update)
    .limit(5).all())

if has_same == 0:

    session.add(m)

    session.commit()

session.close()

datas = session.query(Moment).all()

for data in datas:
    print(data)