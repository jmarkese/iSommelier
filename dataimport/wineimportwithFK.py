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
        try:   
            cursor.execute("SELECT id FROM winereviews_winery WHERE concat(name)=%s;", [row[4]])
            winery_id = cursor.fetchone()
            if winery_id is None:
                winery_id = 1;
            cursor.execute("SELECT id FROM winereviews_variety WHERE concat(name)=%s;", [row[5]])
            variety_id = cursor.fetchone()
            if variety_id is None:
                variety_id = 1;
            values = [row[0],row[1],row[2],row[3], variety_id, winery_id, row[5]]
            cursor.execute('INSERT INTO winereviews_wine(id, name, price, description, variety_id , winery_id, varietal, created_at, updated_at ) VALmydb.commit()UES(%s,%s,%s,%s,%s,%s,%s, NOW(),NOW())', values)
            if row[0] % 1000 == 0 or int(row[0]) == 129970:
                mydb.commit()
        except:
            print (row[5])
cursor.close()
