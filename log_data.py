import threading
import time
import Queue
import random
import string
import sys
import MySQLdb as mdb
from datetime import datetime
import serial

def collectData(input_queue, stop_event):
    ser = serial.Serial()
    ser.port = "/dev/ttyAMA0"
    ser.baudrate = 57600
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1 
    
    print "[collection thread] Opening serial port..."
    ser.open()
    print "[collection thread] Done."

    while not stop_event.is_set():
        data = ser.readline()
        if data:
            data = data.strip("\r\n")
            input_queue.put(data)

    input_queue.put(None) # send a signal telling the logging thread we're done
    print "[collection thread] Terminated data collection."
    return

def logData(input_queue):
    
    # make the database connection
    try:
        con = mdb.connect('localhost', 'edatauser', 'wibble23wobble', 'edata');
        cur = con.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    # log the data
    while True:
        d = input_queue.get()
        if d is None:
            input_queue.task_done()
            print "[logging thread] Finished logging."
            con.close()
            return
 
        if d.startswith("DATA:"):
            data = d[4:] # remove 'DATA:'
            timestamp = datetime.now()
            sql_query = '''INSERT INTO example(data, remotedatetime, uploaded) 
                               VALUES('%s', '%s', '%s')''' % (data, timestamp, '0')
            with con:
                cur = con.cursor(mdb.cursors.DictCursor)
                cur.execute(sql_query)
                input_queue.task_done()


def main():
    input_queue = Queue.Queue()
 
# used to signal termination to the thread
    stop_event = threading.Event() 

# start the logging and data collection threads    
    print "[main] Starting data collection thread..."
    collection_thread = threading.Thread(target=collectData, args=(input_queue, stop_event))
    collection_thread.start()
    print "[main] Done."

    print "[main] Starting logging thread..."
    logging_thread = threading.Thread(target=logData, args=(input_queue,))
    logging_thread.start()
    print "[main] Done."

# listen for keyboard interrupts
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        # stop data collection. Let the logging thread finish logging everything in the queue
        stop_event.set()
        collection_thread.join()
        logging_thread.join()
        
main()
