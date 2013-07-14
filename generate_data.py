import serial
import time

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
        print "Writing data...",
        ser.write("DATA: blah blah blah blah\r\n")
        print "Done"
        time.sleep(2)

main()
