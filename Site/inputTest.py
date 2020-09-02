import pg8000

def connect():
    db = pg8000.connect("postgres", 
        password="Falcon2019", 
        host='35.199.36.16', 
        port=5432, 
        database='rocket_club')
    return db

def main():
    db = connect()
    member_id = 9999
    name = 'Test Name'
    team = 'Test Team'
    division = 0
    command = "INSERT INTO members(member_id, name, team, division) VALUES(%i,'%s','%s',%i)" % (member_id,name,team,division)
    print(command)
    db.run(command)
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
