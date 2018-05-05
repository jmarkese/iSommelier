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
cursor.execute('DROP TABLE IF EXISTS nlp_variety_synonyms;')
mydb.commit()
cursor.execute('CREATE TABLE nlp_variety_synonyms (variety varchar(32), synonym varchar(32), PRIMARY KEY (variety, synonym));')
mydb.commit()
cursor.execute('CREATE INDEX idx_nlp_variety_synonyms__variety ON nlp_variety_synonyms (variety)')
mydb.commit()

with open('variety_synonyms.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        varieties = row[0].split('/')
        for variety in varieties:
            variety = variety.strip()
            for synonym in row[1].split(','):
                synonym = synonym.strip()
                values = [variety, synonym]
                try:
                    if synonym != "":
                        cursor.execute('INSERT INTO nlp_variety_synonyms(variety, synonym) VALUES(%s,%s)', values)
                        mydb.commit()
                except:
                    continue
cursor.execute('REPLACE INTO nlp_variety_synonyms (variety, synonym)  SELECT A.synonym, B.synonym FROM nlp_variety_synonyms A JOIN nlp_variety_synonyms B ON A.variety = B.variety AND A.synonym != B.synonym;')
mydb.commit()
cursor.execute('REPLACE INTO nlp_variety_synonyms (variety, synonym) SELECT synonym, variety FROM nlp_variety_synonyms;')
mydb.commit()


cursor.close()
