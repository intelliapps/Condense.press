#!/usr/bin/python

from newspaper import Article
import mysql.connector as mariadb
from newspaper import ArticleException
import articleDateExtractor

# database credentials to be added.
mariadb_connection = mariadb.connect(user='', password='', database=' ')
cursor = mariadb_connection.cursor()

#retrieving information

cursor.execute("SELECT url FROM skcript")
data=cursor.fetchall()
for text in data:
    try:
	    url=text[0]
	    article = Article(url)
	    article.download()
	    article.parse()
	    try:
	        cursor.execute("UPDATE skcript set author={!a},charCount='{:d}',title={!a} where url='{!s}'".format("".join(article.authors),len(article.text),article.title,url))
	    except mariadb.Error as error:
              print("Error: {}".format(error))
	    d = articleDateExtractor.extractArticlePublishedDate(url)
	    try:
	       cursor.execute("UPDATE skcript set date='{:%Y-%m-%d}'".format(d))
	    except (TypeError, mariadb.Error):
	       print("date error")
    except ArticleException:
	     continue



mariadb_connection.commit()


mariadb_connection.close()










