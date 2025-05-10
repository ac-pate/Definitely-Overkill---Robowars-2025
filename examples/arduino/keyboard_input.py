import serial
import keyboard
import time

# set this to your arduino's serial port
SERIAL_PORT = 'COM6'  # or '/dev/ttyUSB0' on Linux/Mac
BAUD_RATE = 115200

# open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for arduino to reset

print("Control with arrow keys. Press ESC to exit.")

try:
    while True:
        if keyboard.is_pressed("up"):
            ser.write(b'w')
            time.sleep(0.1)
        elif keyboard.is_pressed("left"):
            ser.write(b'a')
            time.sleep(0.1)
        elif keyboard.is_pressed("right"):
            ser.write(b'd')
            time.sleep(0.1)
        elif keyboard.is_pressed("down"):
            ser.write(b's')
            time.sleep(0.1)
        elif keyboard.is_pressed("esc"):
            print("Exiting...")
            break
except KeyboardInterrupt:
    pass
finally:
    ser.close()
