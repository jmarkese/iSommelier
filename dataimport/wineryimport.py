import csv
import MySQLdb
import getpass

user_in = 'keytotalers' #input("Username:")
passwd_in = 'i50mmelier' #getpass.getpass('Password:')
mydb = MySQLdb.connect(host='localhost',
    user=user_in,
    passwd=passwd_in,
    db='isommelier')
cursor = mydb.cursor()

with open('Winery.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        values = [row[0].encode('utf-8'),row[1].encode('utf-8'),row[2].encode('utf-8'),row[3].encode('utf-8')]
        cursor.execute('INSERT INTO winereviews_winery (name, region, province, country, created_at, updated_at) VALUES(%s,%s,%s,%s,NOW(),NOW())', values)
        mydb.commit()

cursor.close()
