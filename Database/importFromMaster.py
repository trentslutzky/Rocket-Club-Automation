import pg8000
import pgTool as pgtool
from pgTool import db
import RCData as rcdata

master_sheet_id = '1hkkeTR4r6Lb8uzqao_0Z2_8k6xrajvtUY4oq2t_Iyk8'


def main():
    master_data = rcdata.get_cells(master_sheet_id,'A2:P')
    id_index = 0
    base_index = 15

    for row in master_data:
        if master_data.index(row) > 0:
            member_id = row[id_index]
            base_rf = row[base_index]
            print(member_id)
            if(int(base_rf) > 0):
                pgtool.add_rf_transaction(int(member_id),'other','',int(base_rf))

if __name__ == '__main__':
    main()
