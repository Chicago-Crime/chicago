import cx_Oracle
from pprint import pprint
from app import app

def getAll():
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM crime")
    for x in cur:
        return (x[0])
        break
    con.close()

def s1mple1():
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []
    cur.execute("SELECT type_of_crime, round(100*(COUNT(*) / SUM(COUNT(*)) OVER ()),2) perc FROM crime GROUP BY type_of_crime")
    for x in cur:
        record.append(x)

    con.close()
    return record

def s1mple2():
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []
    cur.execute("SELECT COUNT(*) FROM CRIME WHERE EXTRACT(YEAR FROM date_of_crime) BETWEEN 2001 and 2005")
    for x in cur:
        record.append(x[0])

    cur.execute("SELECT COUNT(*) FROM CRIME WHERE EXTRACT(YEAR FROM date_of_crime) BETWEEN 2006 and 2010")
    for x in cur:
        record.append(x[0])

    cur.execute("SELECT COUNT(*) FROM CRIME WHERE EXTRACT(YEAR FROM date_of_crime) BETWEEN 2011 and 2015")
    for x in cur:
        record.append(x[0])

    cur.execute("SELECT COUNT(*) FROM CRIME WHERE EXTRACT(YEAR FROM date_of_crime) BETWEEN 2016 and 2019")
    for x in cur:
        record.append(x[0])

    return record
    con.close()

#s1mple3 (heat map under construction *bonus query* xd)

def complex1(year1, year2):
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []
    cur.execute("SELECT ROUND(100*(x.c-y.c)/x.c,2) decline FROM (SELECT COUNT(*) c FROM crime WHERE EXTRACT(YEAR FROM date_of_crime)='{0}') x CROSS JOIN (SELECT COUNT(*) c FROM crime WHERE EXTRACT(YEAR FROM date_of_crime)='{1}') y".format(year1, year2))
    for x in cur:
        record.append(x)

    return record
    con.close()

def complex2(year1, year2):
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []

    cur.execute("SELECT x.type_of_crime, ROUND(100*(x.c-y.c)/x.c,2) decline FROM(SELECT type_of_crime, COUNT(*) c FROM crime WHERE EXTRACT(YEAR from date_of_crime)='{0}' GROUP BY type_of_crime) x, (SELECT type_of_crime, COUNT(*) c FROM crime WHERE EXTRACT(YEAR from date_of_crime)='{1}' GROUP BY type_of_crime) y WHERE x.type_of_crime=y.type_of_crime AND x.c>y.c ORDER BY decline DESC".format(year1, year2))
    for x in cur:
        record.append(x)

    return record
    con.close()

def complex3(crime_value):
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []
    cur.execute("SELECT EXTRACT(HOUR FROM date_of_crime), COUNT(*) count_crime FROM crime WHERE EXTRACT(YEAR from date_of_crime) BETWEEN 2018 and 2019 AND type_of_crime ='" + crime_value + "' GROUP BY EXTRACT(HOUR FROM date_of_crime) ORDER BY EXTRACT(HOUR FROM date_of_crime)")
    for x in cur:
        record.append(x)

    return record
    con.close()

def complex4(year):
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []

    cur.execute("SELECT x.pdistrict_id, ROUND(100*y.c/x.c, 2) perc_arrest FROM(SELECT pdistrict_id, COUNT(*) c FROM crime WHERE EXTRACT(YEAR FROM date_of_crime)=2018 GROUP BY pdistrict_id) x, (SELECT pdistrict_id, COUNT(*) c FROM crime WHERE arrest='TRUE' AND EXTRACT(YEAR FROM date_of_crime)=2018 GROUP BY pdistrict_id) y WHERE x.pdistrict_id=y.pdistrict_id ORDER BY perc_arrest DESC")
    for x in cur:
        record.append(x)

    return record
    con.close()

def complex5():
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []

    cur.execute("SELECT x.ward_id, ROUND(10000*(a/wpopulation_2000 - b/wpopulation_2010),2) safer FROM(SELECT w.ward_id, w.wpopulation_2000, count(*) a FROM ward w, crime c where w.ward_id=c.ward_id AND EXTRACT(YEAR FROM date_of_crime)=2002 GROUP BY (w.ward_id, w.wpopulation_2000)) x, (SELECT w.ward_id, w.wpopulation_2010, count(*) b FROM ward w, crime c where w.ward_id=c.ward_id AND EXTRACT(YEAR FROM date_of_crime)=2010 GROUP BY (w.ward_id, w.wpopulation_2010)) y WHERE x.ward_id=y.ward_id AND (a/wpopulation_2000 - b/wpopulation_2010)>0 ORDER BY safer DESC")
    for x in cur:
        record.append(x)

    return record
    con.close()

def complex6():
    connector = 'rwanare/'+app.config['PASSWORD']+'@oracle.cise.ufl.edu:1521/orcl'
    con = cx_Oracle.connect(connector)
    cur = con.cursor()
    record = []

    cur.execute("SELECT x.type_of_crime, crimes, arrests, ROUND(100*arrests/crimes,2) perc_arrests FROM(SELECT type_of_crime, count(*) crimes FROM crime GROUP BY type_of_crime) x, (SELECT type_of_crime, count(*) arrests FROM crime WHERE arrest='TRUE' GROUP BY type_of_crime) y WHERE x.type_of_crime=y.type_of_crime ORDER BY perc_arrests DESC")
    for x in cur:
        record.append(x)

    return record
    con.close()
