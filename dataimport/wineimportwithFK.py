import csv
import MySQLdb
import getpass

user_in = input("Username:")
passwd_in = getpass.getpass('Password:')
mydb = MySQLdb.connect(host='localhost',
    user=user_in,
    passwd=passwd_in,
    db='isommelier')
mydb.set_character_set('utf8')
cursor = mydb.cursor()

cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

with open('Wine.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        cursor.execute("SELECT id FROM winereviews_winery WHERE name=%s;", [row[5]])
        winery_id = cursor.fetchone()
        cursor.execute("select id from winereviews_variety where name =%s;" [row[6]])
        variety_id = cursor.fetchone()
        values = [row[1],row[2],row[3],row[4], variety_id, winery_id, row[6]]
        cursor.execute('INSERT INTO winereviews_wine(id, name, price, description, variety_id , winery_id, varietal, created_at, updated_at ) VALUES(%s,%s,%s,%s,%s,%s,%s, NOW(),NOW())', values)

mydb.commit()
cursor.close()
