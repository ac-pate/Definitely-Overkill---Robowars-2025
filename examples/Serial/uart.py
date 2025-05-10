#!/usr/bin/python3
import time
import serial
import threading
import sys

print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")

try:
    serial_port = serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    # Wait a second to let the port initialize
    time.sleep(1)

    print("Type Message\n")

    def read_uart():
        while True:
            if serial_port.in_waiting > 0:
                data = serial_port.read(serial_port.in_waiting)
                print(f"\r[from arduino] {data.decode(errors='ignore')}", end='\n', flush=True)

    uart_thread = threading.Thread(target=read_uart, daemon=True)
    uart_thread.start()

    while True:
        user_input = input("> ")
        serial_port.write((user_input + "\n").encode())


except KeyboardInterrupt:
    print("Exiting Program")

except Exception as e:
    print("Error occurred. Exiting Program")
    print("Error: ", e)

finally:
    serial_port.close()