import serial
import time
import random
import string

def main():
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB0'
    ser.baudrate = 57600
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = None   # reads will be blocking

    ser.open()
    print ser.isOpen()

    while True:
        # generate a random string
        lst = [random.choice(string.ascii_letters) for n in xrange(random.randint(15,40))]
        data = "".join(lst)

        print "Writing data...",
        ser.write(data)
        print "Done"
        time.sleep(random.randint(1, 6))

main()
