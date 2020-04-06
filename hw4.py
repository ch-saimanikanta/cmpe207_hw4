import sys
import mysql.connector
import memcache
from timeit import default_timer as timer


memc = memcache.Client(['127.0.0.1:11211'], debug=1);
try:
    mydb = mysql.connector.connect(user='root', password='root',
                                   host='127.0.0.1', database='Cisco')
except mysql.connector.Error  as e:
     print ("Error %d: %s" % (e.args[0], e.args[1]))
     sys.exit (1)
last_month_hire = memc.get('last_month_hire')
if not last_month_hire:
    start = timer()
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM Cisco.Employee where emp_hire_date = "1998-06-13 00:00:00";')
    rows = cursor.fetchall()
    print(rows)
    memc.set('last_month_hire',rows,100)
    print ("Updated memcached with MySQL data")
    end = timer()
    total_time = end - start
    print("Time taken to read my MySQL without Memcache: ",str(total_time))
else:
    start = timer()
    print ("Loaded data from memcached")
    for row in last_month_hire:
        print ("%s, %s,%s,%s,%s,%s,%s,%s" % (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    end = timer()
    total_time = end - start
    print("Time taken to read my MySQL with Memcache: ", str(total_time))
