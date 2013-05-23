from BayesRedis import Classifier
import mysql.connector, unicodedata

# BayesRedis Setup
b = Classifier({
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0
})

# MySQL Setup - Change The Values below to your setup
m = mysql.connector.connect(user='', password='', database='')
cursor = m.cursor()
sql = "SELECT review_text, review_by FROM reviews ORDER BY id"
cursor.execute(sql)

i = 0
for (review_text, review_by) in cursor:
    b.train(review_text.encode('ascii', 'ignore'), review_by.encode('ascii', 'ignore'))
    i = i + 1

print "Total trained: %d" % i