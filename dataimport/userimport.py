import csv
import MySQLdb
import getpass

user_in = input("Username:")
passwd_in = getpass.getpass('Password:')
mydb = MySQLdb.connect(host='localhost',
    user=user_in,
    passwd=passwd_in,
    db='isommelier')
cursor = mydb.cursor()

with open('users_cleaned.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        cursor.execute('INSERT INTO auth_user(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', row)

mydb.commit()
cursor.close()
