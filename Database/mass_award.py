import RCData as rcdata
import pgTool as pgtool 

page_id = '1-Vt1ablMmD-M00Sm_YaPVTDTUUt-XQdisEDs6Na924c'

data_range = 'B2:D'

data = rcdata.get_cells(page_id,data_range)

new_data = []

db = pgtool.db
db.run("SET TIMEZONE='EST'")

for row in data:
    member_id = row[0]
    award = row[1]
    updated = False
    if len(row) > 2:
        if row[2] == 'TRUE':
            updated = True
    else:
        updated = False
    
    if updated == False:
        member_uuid = pgtool.get_member_uuid(member_id)
        if member_uuid != -1:
            db.run(f"INSERT INTO member_awards(member_uuid,award) VALUES('{member_uuid}','{award}')")
            updated = True
            print(member_id,award,updated)

    new_data.append([member_id,award,updated])

db.commit()
db.close()
rcdata.set_cells(page_id,data_range,new_data)
