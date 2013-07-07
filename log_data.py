import threading
import time
import Queue
import random
#import serial


## TODO serial stuff - have to figure out some way of simming ##
#serialport = serial.Serial("/dev/ttyS0", 57600, timeout=0.5)
#serialport.write("write some data here?")
#response = serialport.readlines(None)
#print response

def simSerialPort(input_queue):
    ''' this provides some output simulating the serial
    data from the data logging hardware. 
    '''
    n = 0
    # while n < 10
    while True:
        input_queue.put("DATA: <here are some random data>")
        time.sleep(random.randint(0,10))
        n += 1


def loggingThread(input_queue):
    n = 0

    # this finishes after 10 lines are recieved. This is to allow
    # the program to terminate. In production, will probably want to 
    # use 
    while True:
    #while n < 10:
        d = input_queue.get()
        if d.startswith("DATA:"):
            print d
        input_queue.task_done()
        n += 1
    return


def main():
    input_queue = Queue.Queue()
    
    print "Starting data collection thread...",
    collection_thread = threading.Thread(target=simSerialPort, args=(input_queue,))
    collection_thread.start()
    print("Done.")

    print "Starting logging thread...",
    logging_thread = threading.Thread(target=loggingThread, args=(input_queue,))
    logging_thread.start()
    print("Done.")


main()
