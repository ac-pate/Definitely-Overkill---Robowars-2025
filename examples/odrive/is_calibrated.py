#!/usr/bin/env python3

import odrive
from odrive.enums import *
import time

# Find the connected ODrive (this will block until you connect one)
print("\r\nFinding an ODrive...")
odrv0 = odrive.find_any()

# Erase Current Configuration (Optional, comment out if not needed)
# my_drive.erase_configuration()

print("\r\nODrive Found")
print("Bus voltage is: " + str(odrv0.vbus_voltage) + "V")

# Ensure that the motor is properly referenced through the axis
axis = odrv0.axis0  # You can change axis0 to axis1 if using the second axis

# Configure motor parameters
axis.motor.config.pole_pairs = 7  # Set pole pairs to 7 for your motor
axis.motor.config.resistance_calib_max_voltage = 5.0  # Max voltage for motor resistance calibration
axis.sensorless_estimator.config.pm_flux_linkage = 0.000467228  # Correct for your motor (assuming this value is accurate)

# Start motor calibration
print("\r\nRequesting motor calibration...")
axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION

# Wait for calibration to complete
time.sleep(5)

# Check if motor is calibrated
if axis.motor.is_calibrated:
    print("Motor successfully calibrated!")
else:
    print("Motor calibration failed!")

# Now calibrate the sensorless estimator (this is essential for sensorless control)
print("\r\nRequesting sensorless estimator calibration...")
axis.requested_state = AXIS_STATE_SENSORLESS_CONTROL

# Check sensorless estimator status
print("\r\nSensorless estimator errors:")
print(hex(axis.sensorless_estimator.error))

# Final motor status
print("\r\nMotor is calibrated: ", axis.motor.is_calibrated)

# Print motor errors (if any)
print("\r\nAxis errors are:")
print(hex(axis.error))
print("Motor errors are:")
print(hex(axis.motor.error))
print("Encoder errors are:")
print(hex(axis.encoder.error))
