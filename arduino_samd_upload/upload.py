# Use this in place of bossac to allow for programming arduinos
# All* args passed to the call of this file will be passed to bossac
# * com port will be determined by this script

# Process:
#  1. Preform a reset of the arduino to enter programming mode
#     - Open/Close serial terminal at 1200 baud
#  2. Look for new serial port (arduino in prgm mode)
#  3. Pass that new port to bossac

import serial
import serial.tools.list_ports
import serial.serialutil
import sys
import time
import subprocess

PATH_TO_BOSSAC = "C:\\Users\\benne\\AppData\\Local\\Arduino15\\packages\\arduino\\tools\\bossac\\1.7.0-arduino3\\bossac.exe"

if __name__ == "__main__":
    # Check arg lenth
    if len(sys.argv) < 2:
        print("No arguments given")
        exit(1)

    str_args = ""
    for arg in sys.argv[1:]:
        if ' ' in arg:
            str_args += "\"" + arg + "\"" + ' '
        else:
            str_args += arg + ' '

    # Check to make sure anthing else won't be run by accident
    if '&&' in str_args:
        print("Check input args")
        exit(1)

    i = str_args.find('--port=')
    ser_port = ""
    # Can't find --port so look for -p
    if i < 0:
        i = str_args.find('-p') + 3

        # Can't find any port tag
        if i < 0:
            print("No port specified")
            exit(1)
    
    # Found using --port
    else:
        i += 7
    
    ser_port = str_args[i:].split(' ')[0]

    # Step 0: Get pid for specified device
    ser_list = serial.tools.list_ports.comports()
    dev_pid = 0
    found = False
    for dev in ser_list:
        if dev.name == ser_port:
            dev_pid = dev.pid
            found = True
            break

    if not found:
        print(f"Cannot find port {ser_port}")
        exit(1)

    print(f"Using device {ser_port} (PID={'0x' + hex(dev_pid)[2:].zfill(4)})")

    # Step 1: Reset arduino
    print(f"Resetting device {ser_port}")
    try:
        ser = serial.Serial(ser_port, 1200)
        ser.close()
    except serial.serialutil.SerialException as e:
        print(e)
        exit(1)

    # Step 2: Look for new COM Ports
    ser_new_port = ""
    tries = 3
    while ser_new_port == "" and tries > 0:
        print(f"Searching for new device (PID={'0x' + hex(dev_pid & 0x7FFF)[2:].zfill(4)}...)")
        ser_list = serial.tools.list_ports.comports()
        for dev in ser_list:
            # It looks to be that bit 15 is set to 0 when in pgm mode
            # For MKRZero: 0x804F -> 0x004F
            if dev.pid == dev_pid & 0x7FFF:
                ser_new_port = dev.name
        
        time.sleep(5) # Wait 
        tries -= 1

    # Step 3: call bossac with new port
    if ser_new_port == "":
        print("Cannot find new port :(")
        exit(2)

    bossac_args = str_args.replace(ser_port, ser_new_port)

    print(f"{PATH_TO_BOSSAC} {bossac_args}")
    # subprocess.run(PATH_TO_BOSSAC, bossac_args)
    print(subprocess.Popen(f"{PATH_TO_BOSSAC} {bossac_args}", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8'))

        

