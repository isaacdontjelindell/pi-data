#!/usr/local/bin/python

import MySQLdb as mdb
import sys
import requests

USERNAME = 'testuser'
PW = 'summerD82'
HOST = 'http://lumafile.com/uploaddev/'

def main():
    try:
        con = mdb.connect('localhost', 'edatauser', 'wibble23wobble', 'edata')
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    sql_query = '''SELECT * FROM example WHERE uploaded = 0'''
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(sql_query)
        records = cur.fetchall()

    for record in records:
        payload = {'username':USERNAME,
                   'password':PW,
                   'data':record['data'],
                   'remotedatetime':record['remotedatetime']}
        try:
            response = requests.post(HOST, data=payload)

            if response.status_code == 200:
                sql = ''' UPDATE example SET uploaded = 1 WHERE id = %s ''' % record['id']
                with con:
                    cur = con.cursor(mdb.cursors.DictCursor)
                    cur.execute(sql)
            else:
                print "POST request for record with id = %s failed!" % record['id']
        except:
            print "Something wicked happened with the POST request!"

    con.close()

main()
