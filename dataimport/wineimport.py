import csv
import MySQLdb
import getpass

user_in = 'keytotalers' #input("Username:")
passwd_in = 'i50mmelier' #getpass.getpass('Password:')
mydb = MySQLdb.connect(host='localhost',
    user=user_in,
    passwd=passwd_in,
    db='isommelier')
mydb.set_character_set('utf8')
cursor = mydb.cursor()

cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

with open('winemag-data-130k-v2-clean.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        try:
            # setup the vars
            country = row[1].encode('utf-8')
            province = row[6].encode('utf-8')
            region = row[7].encode('utf-8')
            winery_name = row[13].encode('utf-8')
            variety_name = row[12].encode('utf-8')
            wine_name = row[3].encode('utf-8')
            price = row[5]
            description = row[11].encode('utf-8')
            varietal = row[12].encode('utf-8')
            
            # lookup existing wine
            cursor.execute("SELECT id FROM winereviews_wine WHERE description=%s;", [description])
            wine_id = cursor.fetchone()
            
            # continue if its not there already
            if wine_id is None:

                cursor.execute("SELECT id FROM winereviews_winery WHERE country=%s AND province=%s AND region=%s AND name=%s;", [country, province, region, winery_name])
                winery_id = cursor.fetchone()
        
                if winery_id is None:
                    winery_id = 1
        
                cursor.execute("SELECT id FROM winereviews_variety WHERE name=%s;", [variety_name])
                variety_id = cursor.fetchone()
        
                if variety_id is None:
                    variety_id = 1
        
                values = [wine_name, price, description, variety_id, winery_id, ""]
                cursor.execute('INSERT INTO winereviews_wine(name, price, description, variety_id , winery_id, varietal, created_at, updated_at ) VALUES(%s,%s,%s,%s,%s,%s,NOW(),NOW())', values)
                mydb.commit()
                
        except Exception as e:
            print(e)
            
cursor.close()
