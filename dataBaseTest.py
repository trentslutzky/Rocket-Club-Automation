import RCData as rcdata
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Falcon2019",
  database="rocket_club"
)

cursor = mydb.cursor(dictionary=True)


data_import = rcdata.get_cells('1UkJKMY735oTSohu8X5eM_rvFp267KBbaEiVg4SXaki8','A2:E1000')

id_col = data_import[0].index('member_id')
rf_col = data_import[0].index('total_rf')

for row in data_import:
    if row[id_col] != 'member_id':
        mid = row[id_col]   
        mrf = row[rf_col]
        val = (int(mrf),int(mid))
        sql = 'update member_total_rf set total_rf=%s where id=%s;'
        cursor.execute(sql,val)

mydb.commit()

print(cursor.rowcount, "record inserted.")

