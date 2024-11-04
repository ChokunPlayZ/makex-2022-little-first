# codes make you happy
import novapi
from mbuild.smartservo import smartservo_class
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.encoder_motor import encoder_motor_class
import math
import time

# initialize variables
brushless_state = 0
pos_x = 0
pos_y = 0
enable_automatic = 0

# new class
GRIPPER = smartservo_class("M5", "INDEX1")

distance_sensor_1 = ranging_sensor_class("PORT2", "INDEX1")
distance_sensor_2 = ranging_sensor_class("PORT2", "INDEX2")
distance_sensor_3 = ranging_sensor_class("PORT2", "INDEX3")

FL_ENCODER_M1 = encoder_motor_class("M1", "INDEX1")
FR_ENCODER_M2 = encoder_motor_class("M2", "INDEX1")
BR_ENCODER_M3 = encoder_motor_class("M3", "INDEX1")
BL_ENCODER_M4 = encoder_motor_class("M4", "INDEX1")


def Stop():
    power_expand_board.set_power("DC1", 0)
    power_expand_board.set_power("DC2", 0)
    power_expand_board.set_power("DC3", 0)
    power_expand_board.set_power("DC4", 0)
    power_expand_board.set_power("DC5", 0)
    power_expand_board.set_power("DC6", 0)
    power_expand_board.set_power("DC7", 0)
    power_expand_board.set_power("DC8", 0)
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    FL_ENCODER_M1.set_power(0)
    FR_ENCODER_M2.set_power(0)
    BR_ENCODER_M3.set_power(0)
    BL_ENCODER_M4.set_power(0)

def Brushless_ON():
    global brushless_state
    brushless_state = 1
    power_expand_board.set_power("BL2", 100)
    power_expand_board.set_power("BL1", 100)

def Brushless_OFF():
    global brushless_state
    brushless_state = 0
    power_expand_board.stop("BL1")
    power_expand_board.stop("BL2")

def Auto_Stage():
    power_expand_board.set_power("DC1", 100)
    time.sleep(2)
    power_expand_board.stop("DC1")
    if distance_sensor_1.get_distance() < distance_sensor_2.get_distance():
        Right_Automatic_Stage()
    else:
        Left_Automatic_Stage()

def Manual_Stage():
    if gamepad.is_key_pressed("Right"):
        FL_ENCODER_M1.set_power(50)
        FR_ENCODER_M2.set_power(50)
        BR_ENCODER_M3.set_power(50)
        BL_ENCODER_M4.set_power(50)
    elif gamepad.is_key_pressed("Left"):
        FL_ENCODER_M1.set_power(-50)
        FR_ENCODER_M2.set_power(-50)
        BR_ENCODER_M3.set_power(-50)
        BL_ENCODER_M4.set_power(-50)
    elif gamepad.is_key_pressed("Up"):
        FL_ENCODER_M1.set_power(75)
        BR_ENCODER_M3.set_power(-75)
    elif gamepad.is_key_pressed("Down"):
        FL_ENCODER_M1.set_power(-75)
        BR_ENCODER_M3.set_power(75)
    else:
        L_Joystick()

    if gamepad.is_key_pressed("N2"):
        Brushless_Control()

    Servo_Control()
    Feeder_Control()
    Gripper_Height_Control()

def L_Joystick():
    ly = gamepad.get_joystick("Ly")
    lx = gamepad.get_joystick("Lx")

    FL_ENCODER_M1.set_power(ly)
    FR_ENCODER_M2.set_power(lx)
    BR_ENCODER_M3.set_power(-ly)
    BL_ENCODER_M4.set_power(-lx)

def Left_Automatic_Stage():
    while not (distance_sensor_3.get_distance() > 77):
        time.sleep(0.001)
        FL_ENCODER_M1.set_power(50)
        BR_ENCODER_M3.set_power(-50)

    FL_ENCODER_M1.set_power(0)
    BR_ENCODER_M3.set_power(0)
    while not (distance_sensor_2.get_distance() > 34):
        time.sleep(0.001)
        FR_ENCODER_M2.set_power(-50)
        BL_ENCODER_M4.set_power(50)

    FR_ENCODER_M2.set_power(0)
    BL_ENCODER_M4.set_power(0)
    time.sleep(0.4)
    BR_ENCODER_M3.set_power(0)
    power_expand_board.set_power("DC1", 100)
    while not (distance_sensor_3.get_distance() > 105):
        time.sleep(0.001)
        FL_ENCODER_M1.set_power(50)
        BR_ENCODER_M3.set_power(-25)

    FL_ENCODER_M1.set_power(0)
    BR_ENCODER_M3.set_power(0)
    power_expand_board.set_power("DC1", 0)
    power_expand_board.set_power("DC2", 50)
    FL_ENCODER_M1.set_power(-50)
    FR_ENCODER_M2.set_power(-50)
    BR_ENCODER_M3.set_power(-50)
    BL_ENCODER_M4.set_power(-50)
    time.sleep(0.7)
    FL_ENCODER_M1.set_power(0)
    FR_ENCODER_M2.set_power(0)
    BR_ENCODER_M3.set_power(0)
    BL_ENCODER_M4.set_power(0)
    Brushless_ON()
    power_expand_board.set_power("DC1", 100)
    time.sleep(5)

def Right_Automatic_Stage():
    while not (distance_sensor_3.get_distance() > 77):
        time.sleep(0.001)
        FL_ENCODER_M1.set_power(50)
        BR_ENCODER_M3.set_power(-50)

    FL_ENCODER_M1.set_power(0)
    BR_ENCODER_M3.set_power(0)
    while not (distance_sensor_1.get_distance() > 34):
        time.sleep(0.001)
        FR_ENCODER_M2.set_power(50)
        BL_ENCODER_M4.set_power(-50)

    FR_ENCODER_M2.set_power(0)
    BL_ENCODER_M4.set_power(0)
    time.sleep(0.4)
    BR_ENCODER_M3.set_power(0)
    power_expand_board.set_power("DC1", 100)
    while not (distance_sensor_3.get_distance() > 105):
        time.sleep(0.001)
        FL_ENCODER_M1.set_power(50)
        BR_ENCODER_M3.set_power(-50)

    FL_ENCODER_M1.set_power(0)
    BR_ENCODER_M3.set_power(0)
    power_expand_board.set_power("DC1", 0)
    FL_ENCODER_M1.set_power(-50)
    FR_ENCODER_M2.set_power(-50)
    BR_ENCODER_M3.set_power(-50)
    BL_ENCODER_M4.set_power(-50)
    time.sleep(0.7)
    FL_ENCODER_M1.set_power(0)
    FR_ENCODER_M2.set_power(0)
    BR_ENCODER_M3.set_power(0)
    BL_ENCODER_M4.set_power(0)
    Brushless_ON()
    power_expand_board.set_power("DC1", 100)
    power_expand_board.set_power("DC2", 50)
    time.sleep(5)

def Feeder_Control():
    if gamepad.is_key_pressed("L1"):
        power_expand_board.set_power("DC1", 100)
    elif gamepad.is_key_pressed("L2"):
        power_expand_board.set_power("DC1", -100)
    else:
        power_expand_board.stop("DC1")

    if gamepad.is_key_pressed("R1"):
        power_expand_board.set_power("DC2", 100)
    elif gamepad.is_key_pressed("R2"):
        power_expand_board.set_power("DC2", -100)
    else:
        power_expand_board.stop("DC2")

def Brushless_Control():
    if brushless_state == 0:
        Brushless_ON()
    else:
        Brushless_OFF()

    time.sleep(0.5)

def Servo_Control():
    if GRIPPER.get_value("current") < 200:
        if gamepad.is_key_pressed("+"):
            GRIPPER.set_power(10)
        elif gamepad.is_key_pressed("≡"):
            GRIPPER.set_power(-10)
        else:
            GRIPPER.set_power(0)
    else:
        GRIPPER.set_power(0)

def Gripper_Height_Control():
    if gamepad.is_key_pressed("N1"):
        power_expand_board.set_power("DC3", 100)
    elif gamepad.is_key_pressed("N3"):
        power_expand_board.set_power("DC3", -100)
    else:
        power_expand_board.stop("DC3")

Stop()
enable_automatic = 1
brushless_state = 0
while True:
    time.sleep(0.001)
    # in this season the power management module is not used, instead they used a button to run the automatic stage
    if gamepad.is_key_pressed("N4"):
        if enable_automatic == 1:
            Auto_Stage()

    Manual_Stage()
