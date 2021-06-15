import pg8000
import secret

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    db.run("set timezone = 'EST'")
    return db

def get_journeys():
    db = connect()
    output = []
    result = db.run("select * from journeys order by cert_order")
    for line in result:
        output.append({'flair':line[3],
                      'id':line[0],
                      'number':line[1],
                      'category':line[2],
                      'certified':False})
    return output

def get_member_journeys(member_uuid):
    entre_journeys = []
    science_journeys = []
    journeys = get_journeys()
    db = connect()
    member_journeys = db.run(f"select cert_id from journey_completions where member_uuid = '{member_uuid}'")
    for j in journeys:
        cert_id = j['id']
        for m in member_journeys:
            if m[0] == cert_id:
                j['certified'] = True
        if j['category'] == 'entre':
            entre_journeys.append(j)
        else:
            science_journeys.append(j)
    output = {'entre_journeys':entre_journeys,
                   'science_journeys':science_journeys}
    return output

if __name__ == '__main__':
    get_member_journeys('619e2d83-b9b6-43fe-bbd2-f148f1d98f76')
