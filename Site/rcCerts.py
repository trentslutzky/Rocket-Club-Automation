# Python scripts for updating/getting/setting rc members certifications.

import pgTool as pgtool
import pg8000

def connect():
    db = pg8000.connect("postgres", 
        password="Falcon2019", 
        host='35.199.36.16', 
        port=5432, 
        database='rocket_club')
    return db

def qprep(db, string):
    db.run("DEALLOCATE ALL")
    result = db.prepare(string)
    return result

def get_certs(category):
    db = connect()
    try:
        ps = qprep(db,'SELECT cert,flair FROM certifications WHERE category=:c')
        result = ps.run(c=category)
        return result
    except:
        return -1
    db.close()

def get_member_certs(member_id):
    member_uuid = pgtool.get_member_uuid(member_id)
    db = connect()
    try:
        ps = qprep(db,'SELECT cert FROM member_certs WHERE member_uuid=:u')
        result = ps.run(u=member_uuid)
        return result
    except:
        return -1
    db.close()

def update_certs(member_id, certs):
    print('Updating certs for',member_id)
    member_uuid = pgtool.get_member_uuid(member_id)
    # clear current members certs to update them.
    db = connect()
    command = ("DELETE FROM member_certs WHERE member_uuid='%s'" % (member_uuid))
    db.run(command)
    print('CERTS:',certs)
    for cert in certs:
        command = ("INSERT INTO member_certs(member_uuid,cert) VALUES('%s','%s')"
        % (member_uuid,cert))
        db.run(command)
    db.commit()

def main():
    print(get_certs('entrepreneurship'))
    print(get_member_certs(4405))

if __name__ == '__main__':
    main()

