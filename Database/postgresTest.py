import pg8000

db = pg8000.connect("postgres", password="Falcon2019", host='35.199.36.16', port=5432, database='rocket_club')

cursor = db.cursor()

member_id = 4405
teams = ['Supernovas','Astros','Atoms']

#query = "select * from members where member_id='" + str(member_id) + "'"

ps = db.prepare("select * from teams where team_name=:v")

#result = db.run(query)

for team in teams:
    result = ps.run(v=team)
    print(result)




