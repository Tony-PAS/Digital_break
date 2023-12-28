import board
import pwmio
import canio
import time
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import math

min_joystick_value = 0
max_joystick_value = 100
breaking_duty_cycle = 65535 # this value should be 100%.  We can adjust later on if needed lower
joystick_threshold = 25  # adjust this value for joystick threshold

if hasattr(board, 'CAN_STANDBY'):
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)
if hasattr(board, 'BOOST_ENABLE'):
    boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
    boost_enable.switch_to_output(True)

can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=250_000, auto_restart=True)
listener = can.listen(timeout=0.0)
# Define the target CAN ID
TARGET_CAN_ID = 0x18F

# Initialize PWM output needs to eventually be changed to digital output
pwm = pwmio.PWMOut(board.D11, frequency=5000, duty_cycle=0)

while True:
    message = listener.receive()
    if message is not None:
        if message.id == TARGET_CAN_ID:
            # This takes the message from CAN id 0x18F and grabs bytes from 1 and 3
             joy_lr = message.data[1]
             joy_ud = message.data[3]
            #This part of the code applies an offset to joystick to  resting position 127
             if joy_lr >= 128:
                adjusted_joy_lr = joy_lr - 251
             else:
                adjusted_joy_lr = joy_lr
             if joy_ud >= 128:
                adjusted_joy_ud = joy_ud - 255
             else:
                adjusted_joy_ud = joy_ud


             joy_abs = abs(adjusted_joy_ud) #joystick up down converted to an absolute position

             #print("Abs:",joy_abs)
             #print("Raw:",adjusted_joy_ud)



# Set the PWM duty cycle
        if joy_abs >= joystick_threshold:
          pwm.duty_cycle = pwm_duty_cycle
          print("duty = max")
        if joy_abs < joystick_threshold:
          pwm.duty_cycle = 0
          print("duty = 0")
    time.sleep(0.1)  # Adjust as needed
    print("running")


