import threading
import time
import Queue
import random
import sys
#import serial


## TODO serial stuff - have to figure out some way of simming ##
#serialport = serial.Serial("/dev/ttyS0", 57600, timeout=0.5)
#serialport.write("write some data here?")
#response = serialport.readlines(None)
#print response

def sim_collectData(input_queue, stop_event):
    ''' this provides some output simulating the serial
    data from the data logging hardware. 
    '''
    n = 0
    while not stop_event.is_set():
        input_queue.put("DATA: <here are some random data> " + str(n))
        stop_event.wait(0.001)
        n += 1
    input_queue.put(None) # send a signal telling the logging thread we're done
    print "[collection thread] Terminated data collection."
    return


def logData(input_queue):
    n = 0

    # if the stop event is recieved and the previous loop terminates, 
    # finish logging the rest of the items in the queue.
    while True:
        d = input_queue.get()
        if d is None:
            input_queue.task_done()
            print "[logging thread] Finished logging."
            return
        if d.startswith("DATA:"):
            print "[logging thread] Logged to DB: " + d
            input_queue.task_done()
            n += 1


def main():
    input_queue = Queue.Queue()
    
    stop_event = threading.Event() # used to signal termination to the thread
    
    print "[main] Starting data collection thread...",
    collection_thread = threading.Thread(target=sim_collectData, args=(input_queue, stop_event))
    collection_thread.start()
    print "Done."

    print "[main] Starting logging thread...",
    logging_thread = threading.Thread(target=logData, args=(input_queue, ))
    logging_thread.start()
    print "Done."

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        # stop data collection. Let the logging thread finish logging everything in the queue
        stop_event.set()
        collection_thread.join()
        logging_thread.join()

main()
