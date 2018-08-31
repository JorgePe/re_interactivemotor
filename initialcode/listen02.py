#!/usr/bin/env python3

import serial
import time

TTYDEVICE = '/dev/ttyUSB3'
BPS = 115200

STEP = 0.09  # emyric 0.003..0.1
SYNC_TIME = 0.75 # time for the break command
SYNC_ZEROS = 2000 # empyric

MSG_RETRY = b'\xC0\x00\x3F'
BYTE_START = 216  # D8

def recv(ser, x):
    # seen somewhere, need to find author
    data = ser.read(1)
    return data+ser.read(min(x-1, ser.in_waiting))

def initmotor(ser):
    ser.write(b'\x00')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x00')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x00')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x00')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x54')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x22')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x00')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x10')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\x20')
    ser.flush()
    time.sleep(STEP)

    ser.write(b'\xB9')
    ser.flush()
    time.sleep(STEP)

def motor_sync(ser):
    ser.reset_input_buffer()
    ser.reset_output_buffer()

#    ser.send_break(SYNC_TIME*1000)    # does not work

    for i in range(0, SYNC_ZEROS):
        ser.write(b'\x00')
        ser.flush()


ser = serial.Serial(TTYDEVICE)
ser.baudrate = BPS
ser.timeout = 0
ser.write_timeout = 0

if ser.isOpen():
    print("Starting")
    motor_sync(ser)
    start_time = time.time()

    while True:
        try:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(b'\x02')
            ser.flush()
            time.sleep(STEP)

            r = recv(ser,10)
            if r != b'' :
                if r == MSG_RETRY :
                    print("Got ",r,"-> Init")
                    initmotor(ser)
                elif r[0]!= 0 :

                    if r[0] == BYTE_START :
                        print("Speed   :", '{:02X}'.format(r[1]), "(h) = ", r[1],"(d)")
                        print("Position:", '{:02X}'.format(r[2])," ", '{:02X}'.format(r[3]), " ", '{:02X}'.format(r[4]), " ", '{:02X}'.format(r[5]), "= ", end="")
                        print(r[2]+256*r[3]+65536*r[4]+16777216*r[5], " degrees")
                        print("CRC     :", '{:02X}'.format(r[9]), "(h) = ", r[9],"(d)")
                    else:
                        for n in range(0,len(r)):
                            print('{:02X}'.format(r[n]), end="")
                    print()
                else:
                    #print('Got ', r,end="")
                    if time.time() - start_time > SYNC_TIME :
                        print("Timeout -> Resync", end="")
                        motor_sync(ser)
                        start_time = time.time()
                    print()
            else:
                print("Null")

        except:
            ser.close()
            print("End")
            break
