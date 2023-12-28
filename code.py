import board
import pwmio
import canio
import time
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import math

min_joystick_value = 0
max_joystick_value = 100

if hasattr(board, 'CAN_STANDBY'):
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)
if hasattr(board, 'BOOST_ENABLE'):
    boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
    boost_enable.switch_to_output(True)
# can = canio.CAN(rx=board.PB13, tx=board.PB14, baudrate=250_000, auto_restart=True)
can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=250_000, auto_restart=True)
listener = can.listen(timeout=0.0)
# Initialize PWM output
pwm = pwmio.PWMOut(board.D10, frequency=5000, duty_cycle=0)
# Define the target CAN ID
TARGET_CAN_ID = 0x18F
while True:
    message = listener.receive()
    if message is not None:
        if message.id == TARGET_CAN_ID:
            # Example: Assuming the message contains a byte that represents the PWM value
             joy_lr = message.data[1]
             joy_ud = message.data[3]
            # btn_msg = message.data[4]
            # btn_pressed(btn_msg)
            # pwm_value = message.data[0]
            # Scale the value to match the PWM duty cycle range (0-65535)
            #print("Message received with ID:", message.id)
            # pwm.duty_cycle = int((pwm_value / 255) * 65535)
            # Scale the values to the range 0 to 255
             # Apply an offset to shift the resting position to 127
             # Apply two's complement adjustment
             if joy_lr >= 128:
                adjusted_joy_lr = joy_lr - 251
             else:
                adjusted_joy_lr = joy_lr
             if joy_ud >= 128:
                adjusted_joy_ud = joy_ud - 255
             else:
                adjusted_joy_ud = joy_ud
             joy_abs = abs(adjusted_joy_ud)
# Now, the adjusted values should have the resting position at 127
             print("Abs:",joy_abs)
             print("Raw:",adjusted_joy_ud)
             pwm_duty_cycle = int(((max_joystick_value - joy_abs) / (max_joystick_value - min_joystick_value)) * 65535)
            
             # Ensure pwm_duty_cycle is within the valid range (0-65535)
             pwm_duty_cycle = max(0, min(pwm_duty_cycle, 65535))

# Set the PWM duty cycle
             pwm.duty_cycle = pwm_duty_cycle
    time.sleep(0.1)  # Adjust as needed
    #print("running")
