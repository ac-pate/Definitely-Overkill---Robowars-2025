import time
import odrive
from odrive.enums import *

# Connect to the first ODrive device connected over USB
print("Finding ODrive...")
odrv0 = odrive.find_any()

print("ODrive connected!")

# Configuring ODrive for sensorless control
print("Configuring motor...")
odrv0.config.dc_bus_undervoltage_trip_level = 20  # V
odrv0.config.dc_bus_overvoltage_trip_level = 30   # V
odrv0.config.dc_max_positive_current = 50  # A
odrv0.config.dc_max_negative_current = -10  # A

odrv0.axis0.config.motor.pole_pairs = 7
odrv0.axis0.config.motor.torque_constant = 0.01654  # Nm/A
odrv0.axis0.config.motor.current_soft_max = 80.0    # A
odrv0.axis0.config.motor.current_hard_max = 100.0    # A

odrv0.axis0.controller.config.vel_limit = 100.0      # [turn/s]
odrv0.axis0.config.torque_soft_min = -2  # Nm
odrv0.axis0.config.torque_soft_max = 2  # Nm

odrv0.axis0.config.load_encoder = EncoderId.SENSORLESS_ESTIMATOR
odrv0.axis0.config.commutation_encoder = EncoderId.SENSORLESS_ESTIMATOR
odrv0.axis0.config.sensorless_ramp.vel = -50   # [radians/s]
odrv0.axis0.config.sensorless_ramp.accel = 4  # [radians/s^2]

odrv0.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL

# Now let's control the motor!

def set_motor_speed(speed_fraction):
    # Speed fraction should be between -1 (full reverse) and +1 (full forward)
    max_speed = 100  # maximum speed in turns per second
    target_velocity = max_speed * speed_fraction  # velocity in turns per second
    odrv0.axis0.controller.vel_setpoint = target_velocity 
# Test: Run motor at full speed forward (+1), stop (0), reverse (-1)
try:
    print("Running motor forward at full speed...")
    set_motor_speed(1)
    time.sleep(3)

    print("Stopping motor...")
    set_motor_speed(0)
    time.sleep(2)

    print("Running motor reverse at full speed...")
    set_motor_speed(-1)
    time.sleep(3)

    # Stop the motor at the end
    print("Stopping motor...")
    set_motor_speed(0)

except KeyboardInterrupt:
    print("Interrupted. Stopping motor.")
    set_motor_speed(0)

