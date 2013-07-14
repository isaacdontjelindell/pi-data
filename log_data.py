import threading
import time
import Queue
import random
import string
import sys
import MySQLdb as mdb
from datetime import datetime
import serial


## TODO serial stuff - have to figure out some way of simming ##
#serialport = serial.Serial("/dev/ttyS0", 57600, timeout=0.5)
#serialport.write("write some data here?")
#response = serialport.readlines(None)
#print response

def collectData(input_queue, stop_event):
    ser = serial.Serial()
    ser.port = '/dev/ttyAMA0'
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
        print data

    input_queue.put(None) # send a signal telling the logging thread we're done
    print "[collection thread] Terminated data collection."
    return
    

def sim_collectData(input_queue, stop_event):
    ''' this provides some output simulating the serial
    data from the data logging hardware. 
    '''
    while not stop_event.is_set():
        # generate a random string
        lst = [random.choice(string.ascii_letters) for n in xrange(random.randint(15,40))]
        data = "".join(lst)
            
        input_queue.put("DATA:" + data)

        # wait a random time
        stop_event.wait(random.randint(1,5))

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
