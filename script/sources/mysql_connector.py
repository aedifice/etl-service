import os
import pymysql

# run a single SQL query against a MySQL connection
def query_sql(query):
    # currently assumes host is coming from Docker compose
    mysql_connection = pymysql.connect(host = "etl-sql",
                                       user = os.environ['MYSQL_USER'],
                                       password = os.environ['MYSQL_PASSWORD'],
                                       database = os.environ['MYSQL_DATABASE'],
                                       cursorclass = pymysql.cursors.DictCursor)
    
    cursor = mysql_connection.cursor()
    cursor.execute(query)
    query_output = cursor.fetchall()
    mysql_connection.close()

    return query_output
