import RCData as rcdata
import pg8000
import pgTool
from pgTool import db

def get_member_totals():
    ps = db.prepare('SELECT member_id FROM members order by member_id')
    members = ps.run()
    g_members = rcdata.get_cells('1hkkeTR4r6Lb8uzqao_0Z2_8k6xrajvtUY4oq2t_Iyk8','A3:C')
    for m in members:
        member_id = m[0]
        ps = db.prepare('SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a')
        result = ps.run(a=member_id)
        for row in g_members:
            if(row[0] == str(member_id)):
                g_vm = row[2]
        difference = result[0][0] - int(g_vm)
        if(difference != 0):
            print(str(member_id) + ' ' + str(difference))

def main():
    get_member_totals()

if __name__ == '__main__':
    main()

