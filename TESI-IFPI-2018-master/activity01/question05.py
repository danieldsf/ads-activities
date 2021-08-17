from libs.myurllib import session, Team

t = Team(name='malaga', ogol_id = 45, pesstat_id = 29, sofifa_id = 573)

data = session.query(Team).filter(Team.name == 'malaga').limit(5).all()

if(len(data) == 0):
    session.add(t)

session.commit()    

for i in data:
    i.get_from_ogol()
    print(i.asdict())