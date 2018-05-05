import csv
import MySQLdb
import metapy
import getpass


def get_comment_nlp(comment):
    doc = metapy.index.Document()
    doc.content(comment)
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    stop_words = "../isommelier/nlp/lemur-stopwords.txt"
    tok = metapy.analyzers.ListFilter(tok, stop_words, metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    return " ".join(tokens)


user_in = 'keytotalers'  # input("Username:")
passwd_in = 'i50mmelier'  # getpass.getpass('Password:')
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
    i = 0
    for row in reader:

        if i is 0:
            i += 1
            continue

        user_name = row[10]
        description = row[11]
        rating = row[4]
        comment = row[2]
        province = row[6]
        region = row[7]
        winery_name = row[13]
        variety_name = row[12]
        wine_name = row[3]

        cursor.execute("SELECT id FROM auth_user WHERE username=%s;", [user_name])
        user_id = cursor.fetchone()

        # if user_id is None:
        #     user_id = 1

        cursor.execute("SELECT id FROM winereviews_wine WHERE description=%s;", [description])
        wine_id = cursor.fetchone()

        if wine_id is None:
            wine_id = 1

        nlp_data = " ".join([str(user_name), str(wine_name), str(variety_name), str(description), str(comment)])
        comment_nlp = get_comment_nlp(nlp_data)

        values = [comment, user_id, wine_id, rating, comment_nlp]
        # print(values)
        cursor.execute(
            'INSERT INTO winereviews_review(comment, user_id, wine_id, rating, created_at, updated_at, comment_nlp) VALUES(%s,%s,%s,%s,NOW(),NOW(), %s)',
            values)
        mydb.commit()

cursor.close()

