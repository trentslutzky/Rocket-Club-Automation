import mysql.connector

mydb = mysql.connector.connect(
  host="34.86.127.214",
  user="trent",
  password="Falcon9",
  database="rocket_club"
)

cursor = mydb.cursor()

team = 'Supernovas'

cursor.execute("SELECT * FROM members where team='" + team + "'")

result = cursor.fetchall()

print(str(len(result)) + ' Members in ' + team + ':')
for row in result:
    print(row[1])
