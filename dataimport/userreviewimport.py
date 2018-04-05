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

with open('winemag-data-130k-v2-clean.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        user_name = row[10]
        description = row[11]
        rating = row[4]
        comment = row[2]

        cursor.execute("SELECT id FROM auth_user WHERE username=%s;", [user_name])
        user_id = cursor.fetchone()
        
        cursor.execute("SELECT id FROM winereviews_wine WHERE description=%s;", [description])
        wine_id = cursor.fetchone()

        if wine_id is None:
            wine_id = 1

        values = [comment, user_id, wine_id, rating]
        cursor.execute('INSERT INTO winereviews_review(comment, user_id, wine_id, rating, created_at, updated_at ) VALUES(%s,%s,%s,%s,NOW(),NOW())', values)
        mydb.commit()

cursor.close()
