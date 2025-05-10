import serial
import time
import keyboard

# Serial port and baud rate
SERIAL_PORT = 'COM6'  # Update this to the correct COM port
BAUD_RATE = 115200
rampUpEnabled = True  # Ramp-up status flag

# Setup the serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT} at {BAUD_RATE} baud.")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Function to send action and speed to Arduino
def send_command(action):
    # Command is now just a single character to match 'w', 'a', 'd', 's', 'r' from Arduino
    ser.write(action.encode())
    print(f"Sent command: {action}")

# Function to toggle ramp-up
def toggle_ramp_up():
    global rampUpEnabled
    rampUpEnabled = not rampUpEnabled
    print(f"Ramp-up {'enabled' if rampUpEnabled else 'disabled'}.")

# Main loop to monitor keyboard input
while True:
    if keyboard.is_pressed('q'):  # Quit program
        print("Exiting program.")
        break
    if keyboard.is_pressed('r'):  # Toggle ramp-up
        toggle_ramp_up()
        time.sleep(0.2)  # Prevent multiple toggles

    # Movement controls and corresponding actions
    if keyboard.is_pressed('up'):
        send_command('w')  # Forward
        print("Moving forward.")
    elif keyboard.is_pressed('left'):
        send_command('a')  # Spin left
        print("Spinning left.")
    elif keyboard.is_pressed('right'):
        send_command('d')  # Spin right
        print("Spinning right.")
    elif keyboard.is_pressed('down'):  # Stop command
        send_command('s')  # Stop
        print("Stopping robot.")

    # Print status of ramp-up feature
    print(f"Ramp-up is {'enabled' if rampUpEnabled else 'disabled'}.")

    time.sleep(0.1)  # Delay to avoid overloading the CPU
