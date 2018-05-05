import csv
import MySQLdb
import getpass
import metapy

user_in = 'keytotalers' #input("Username:")
passwd_in = 'i50mmelier' #getpass.getpass('Password:')
mydb = MySQLdb.connect(host='localhost',
    user=user_in,
    passwd=passwd_in,
    db='isommelier')
cursor = mydb.cursor()
# try:
#     cursor.execute('ALTER TABLE winereviews_review DROP COLUMN comment_nlp;')
#     mydb.commit()
# except:
#     print("err")
# cursor.execute('ALTER TABLE winereviews_review ADD COLUMN comment_nlp TEXT;')
# mydb.commit()
# cursor.execute('ALTER TABLE winereviews_review ADD FULLTEXT idx__winereviews_review__comment_nlp (comment_nlp);')
# mydb.commit()

if False:
    comment = ""
    id = 1
    doc = metapy.index.Document()
    doc.content(comment)
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    stop_words = "../isommelier/nlp/lemur-stopwords.txt"
    tok = metapy.analyzers.ListFilter(tok, stop_words, metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    comment_nlp = " ".join(tokens)
    cursor.execute('UPDATE winereviews_review SET comment_nlp = %s WHERE id = %s', [comment_nlp, id])
    mydb.commit()

cursor.close()
