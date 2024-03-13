import time
import Controller_state as Cs
import subprocess
import struct
import ctypes
import Shear_memory_C as mem
from threading import Thread
# import PCA_communication as PCA
#

global active_id
global copy_active_id
global width_arm_changing
global width_arm
global width_hand
global width_manipulator_rotation
global width_manipulator
global stepper_do_steps
global changing_motor_mode_active
global multiple_motors
multiple_motors = False
width_arm = [0,307,307,307,297,0,500]


LED_PIN_dict = {0:6,1:9,2:10,3:13,4:15}




# def PWM_arm():
#     while True:
#         # 0.05 - 0.025
#         current_width = Get_width_arm()
#         set_position_arm = 1
#         time.sleep(current_width)
#         set_position_arm = 0
#         time.sleep(0.025 - current_width)
#     return


def diode_blinking_changing_motor():
    currnet_led_state= 0
    while(changing_motor_mode_active):
        for i in range(5):
            if i == copy_active_id:
                result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'{currnet_led_state}'], capture_output=True)
            else:
                result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'0'], capture_output=True)
        time.sleep(0.1)
        if currnet_led_state:
            currnet_led_state = 0
        else:
            currnet_led_state = 1

    for i in range(5):
        if i == active_id:
            result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'1'], capture_output=True)
        else:
            result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'0'], capture_output=True)
    return


def diode_blinking_move_motor():
    while(width_arm_changing[active_id]):
        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[active_id]}',f'1'], capture_output=True)
        time.sleep(0.02)
        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[active_id]}',f'0'], capture_output=True)
        time.sleep(0.1)
        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[active_id]}',f'1'], capture_output=True)
        time.sleep(0.02)
        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[active_id]}',f'0'], capture_output=True)
        time.sleep(0.1)
        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[active_id]}',f'1'], capture_output=True)
        time.sleep(0.5)
    return


def get_current_PWM_signal():
    data = [int(i) for i in (width_arm[1:])]
    return data,multiple_motors ,active_id - 1 


def Buttons_axis(ps4_data: Cs.PS4Controller):
    global active_id
    global width_arm
    global changing_motor_mode_active
    global copy_active_id
    global multiple_motors
    global width_arm_changing
    active_id = 1
    changing_motor_mode_active = False
    width_arm_changing = [False for i in range(5)]

    multiple_motors = False
    # Proces = subprocess.Popen(["../PWM_control/main"], stdin=subprocess.PIPE)
    # PWM_arm_data(1, Proces)

    '''
    0 - obrót korpusu
    1 - ramie
    2 - przedramie
    3 - manipulator obrot
    4 - manipulator szczeki
    '''
    # PCA.restet_all_to0()
    x_button = None
    R1_button = None
    L1_button = None
    copy_active_id = None
    square_button = None
    triangle_button = None
    speed_multiplayer = 0.5
    left_arrow = None
    right_arrow = None
    while True:
        time.sleep(0.1)
        # print(width_arm)
        mm_changed = False
        last_x_button = x_button
        x_button = ps4_data.get_buttons()[2]
        last_R1_button = R1_button
        R1_button = ps4_data.get_triggers_buttons()[2]
        last_L1_button = L1_button
        L1_button = ps4_data.get_triggers_buttons()[0]
        last_square_button = square_button
        square_button = ps4_data.get_buttons()[3]
        l2_axis_pos = ps4_data.get_triggers_axis()[0]
        r2_axis_pos = ps4_data.get_triggers_axis()[1]
        L_x_pos = ps4_data.get_left_stick_pos()[0]
        R_x_pos = ps4_data.get_right_stick_pos()[0]
        last_triangle_button = triangle_button
        triangle_button = ps4_data.get_buttons()[0]
        last_left_arrow = left_arrow
        last_right_arrow = right_arrow
        up_arrow = ps4_data.get_arrows()[0]
        right_arrow = ps4_data.get_arrows()[1]
        down_arrow = ps4_data.get_arrows()[2]
        left_arrow = ps4_data.get_arrows()[3]

        '''
        zmiana aktywnego silnika
        '''

        if not multiple_motors:
            first_loop = False
            if not changing_motor_mode_active:
                copy_active_id = active_id
            if not x_button and last_x_button and not changing_motor_mode_active and not width_arm_changing[active_id]:
                print('Tryb wyboru silnika aktywny')
                
                changing_motor_mode_active = True
                blink = Thread(target = diode_blinking_changing_motor)
                blink.start()
                first_loop = True
            if changing_motor_mode_active and not R1_button and last_R1_button:
                if copy_active_id > 0:
                    copy_active_id -= 1
                else:
                    copy_active_id = 4 
                print(f'Zmiana silnika  {copy_active_id}')
            if changing_motor_mode_active and not L1_button and last_L1_button:
                if copy_active_id < 4:
                    copy_active_id += 1
                else:
                    copy_active_id = 0
                print(f'Zmiana silnika  {copy_active_id}')
            if changing_motor_mode_active and not x_button and last_x_button and not first_loop:
                print(f'Wybrano silnik {copy_active_id}')
                active_id = copy_active_id

                changing_motor_mode_active = False
            if changing_motor_mode_active and ps4_data.get_buttons()[1]:
                print(f'Opuszczono tryb wyboru silnika')
                changing_motor_mode_active = False

            if not changing_motor_mode_active and not width_arm_changing[active_id] and last_triangle_button and not triangle_button:
                multiple_motors = not multiple_motors
                mm_changed = True
                print("steruj wszystkimi silnikami")

                for i in range(5):
                    result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'1'], capture_output=True)



            for i in range(1, 5):
                if active_id == i:
                    if not changing_motor_mode_active and not square_button and last_square_button and not width_arm_changing[i]:
                        width_arm_changing[i] = True
                        blinking_move = Thread(target = diode_blinking_move_motor)
                        blinking_move.start()
                        print(f'Tryb zmiany pozycji serwonapędu {i}')
                    if width_arm_changing[i]:
                        # print(width_arm[i])
                        if last_R1_button and not R1_button and speed_multiplayer > 0.15:
                            speed_multiplayer -= 0.05
                            print('zwiększono precyzję')
                        if last_L1_button and not L1_button and speed_multiplayer < 0.95:
                            speed_multiplayer += 0.05
                            print('zmniejszono precyzję')
                        if 0 < i < 4:
                            if width_arm[i] > 102:
                                width_arm[i] -= ((l2_axis_pos//6+1 )* speed_multiplayer)
                            else:
                                width_arm[i] = 102

                            if width_arm[i] < 512:
                                width_arm[i] += ((r2_axis_pos//6+1) * speed_multiplayer) 
                            else:
                                width_arm[i] = 512
                        if i == 4:
                            if width_arm[i] > 102:
                                width_arm[i] -= ((l2_axis_pos//6+1) * speed_multiplayer)
                            else:
                                width_arm[i] = 102
                            if width_arm[i] < 500:
                                width_arm[i] += ((r2_axis_pos//6+1) * speed_multiplayer) 
                            else:
                                width_arm[i] = 500
                    # print(width_arm[i])
                    update_PWM = Thread(target = mem.update_position, args=[width_arm])
                    update_PWM.start()
                    if width_arm_changing[i] and ps4_data.get_buttons()[1]:
                        width_arm_changing[i] = False
                        print(f'Opuszczono tryb zmiany pozycji: wypełnienie {width_arm[i]} mikro sekund')
                    # else:
                        # PWM_arm_data(0,Proces)
            if active_id == 0 and not square_button and last_square_button:
                if r2_axis_pos > l2_axis_pos:
                    width_arm[0] = 1
                    width_arm[5] = 1
                    width_arm[6] = 500 * speed_multiplayer
                if r2_axis_pos < l2_axis_pos:
                    width_arm[0] = 1
                    width_arm[5] = 0
                    width_arm[6] = 500 * speed_multiplayer
                if (r2_axis_pos < 20 and l2_axis_pos<20) or l2_axis_pos == r2_axis_pos:
                    width_arm[0] = 0
            # update_PWM = Thread(target = PCA.update_PWM_signal,args=[width_arm])
            # update_PWM.start()

            update_stepper = Thread(target = mem.update_position, args=[width_arm])
            update_stepper.start()


        if multiple_motors:
            if not triangle_button and last_triangle_button and not mm_changed:
                print("Metoda jednego silnika")
                for i in range(5):
                    if i == active_id:
                        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'1'], capture_output=True)
                    else:
                        result = subprocess.run(['gpio','write',f'{LED_PIN_dict[i]}',f'0'], capture_output=True)
                multiple_motors = not multiple_motors

            width_arm[1] += (L_x_pos//6) * speed_multiplayer
            if width_arm[1] > 512:
                width_arm[1] = 512
            if width_arm[1] < 102:
                width_arm[1] = 102

            width_arm[2] += (R_x_pos//6) * speed_multiplayer
            if width_arm[2] > 512:
                width_arm[2] = 512
            if width_arm[2] < 102:
                width_arm[2] = 102
            width_arm[3] += (r2_axis_pos//6) * speed_multiplayer
            width_arm[3] -= (l2_axis_pos//6)* speed_multiplayer
            if width_arm[3] > 512:
                width_arm[3] = 512
            if width_arm[3] < 102:
                width_arm[3] = 102
            if up_arrow != 0:
                width_arm[4] += 22 * speed_multiplayer 
            if down_arrow != 0:
                width_arm[4] -= 22 * speed_multiplayer
            if width_arm[4] > 500:
                width_arm[4] = 500
            if width_arm[4] < 102:
                width_arm[4] = 102
            if R1_button:
                width_arm[0] = 1
                width_arm[5] = 1
                width_arm[6] = 500 * speed_multiplayer
            if L1_button:
                width_arm[0] = 1
                width_arm[5] = 0
                width_arm[6] = 500 * speed_multiplayer
            if (R1_button and L1_button) or (not L1_button and not R1_button):
                width_arm[0] = 0

            # update_PWM = Thread(target = PCA.update_PWM_signal,args=[width_arm])
            # update_PWM.start()

            update_stepper = Thread(target = mem.update_position, args=[width_arm])
            update_stepper.start()

            if not left_arrow and last_left_arrow:
                speed_multiplayer += 0.05
                print(f"zwiekszono precyje {speed_multiplayer}")
                if speed_multiplayer > 1:
                    speed_multiplayer = 1
            if not right_arrow and last_right_arrow:
                speed_multiplayer -= 0.05
                print(f"zmniejszono precyzje {speed_multiplayer}")
                if speed_multiplayer < 0.15:
                    speed_multiplayer = 0.10




 








