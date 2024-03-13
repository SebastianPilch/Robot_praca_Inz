import smbus2
import time
# import Motors_control
import Motors_control as Mc
device_addres = 0x40
bus_num = 0
width_channels = {0:0,1:3,2:4,3:7}
bus = smbus2.SMBus(bus_num)



def convert_to_hex(value):
    bige = value // 256
    lit =  value%256
    return bige, lit

def update_PWM_signal(width_data):
    for i in range(4):
        channel = i
        OFF_value_H,OFF_value_L = convert_to_hex(width_data[i])
        base_address = 0x08
        LED_OFF_H = base_address + 4* channel + 1
        LED_OFF_L = base_address +4*channel
        time.sleep(0.002)
        bus.write_byte_data(device_addres, LED_OFF_H,OFF_value_H)
        time.sleep(0.002)
        bus.write_byte_data(device_addres, LED_OFF_L,OFF_value_L)

    return

def update_PWM_signal_one_channel(width_data, index):
    channel = index
    # print(width_data)
    OFF_value_H,OFF_value_L = convert_to_hex(width_data[index])
    base_address = 0x08
    LED_OFF_H = base_address + 4* channel + 1
    LED_OFF_L = base_address +4*channel
    time.sleep(0.002)
    bus.write_byte_data(device_addres, LED_OFF_H,OFF_value_H)
    time.sleep(0.002)
    bus.write_byte_data(device_addres, LED_OFF_L,OFF_value_L)

    return


def restet_all_to0():
    PRE_scaler_add = 0xFE
    Pre_val = 121
    base_address = 0x06
    for channel in range(16): 
        LED_ON_H = base_address + 4*channel + 1
        LED_ON_L = base_address +4*channel
        LED_OFF_H = base_address+ 4*channel+3
        LED_OFF_L = base_address +4*channel +2
        time.sleep(0.002)
        bus.write_byte_data(device_addres, LED_OFF_H,0)
        time.sleep(0.002)
        bus.write_byte_data(device_addres, LED_ON_H,0)
        time.sleep(0.002)
        bus.write_byte_data(device_addres, LED_OFF_L,0)
        time.sleep(0.002)
        bus.write_byte_data(device_addres, LED_ON_L,0)
    time.sleep(0.002)
    # current_mode1 = bus.read_byte_data(device_addres,0x00)
    # time.sleep(0.02)
    bus.write_byte_data(device_addres, PRE_scaler_add,Pre_val)
    time.sleep(0.002)
    bus.write_byte_data(device_addres, 0x00,0x00)
    time.sleep(0.002)
    # bus.write_byte_data(device_addres,0x00, current_mode1 | ~0x80)
    # time.sleep(0.02)
    # bus.write_byte_data(device_addres, 0x00,current_mode1 & ~0x10)
    # time.sleep(0.02)
    # bus.write_byte_data(device_addres,0x00, current_mode1 & ~0x80)
    # time.sleep(0.02)
    return



# restet_all_to0()
# data = conert_to_hex(500)
# print(data)
# while(1):
#     time.sleep(5)
#     try:
#         data =  Motors_control.width_arm
#     except:
#         data = [1,307,307,307,307,307]
#     print(data)
    # update_PWM_signal(data)
# update_PWM_signal(3,data[0],data[1])
# update_PWM_signal(15,data[0],data[1])


def Servo_control():

    restet_all_to0()
    while(1):

        new_data = [1]
        # wejscie = input('podaj pwm')
        new_data, work_mode, index = Mc.get_current_PWM_signal()
        if work_mode:
            update_PWM_signal(new_data)
        else:
            update_PWM_signal_one_channel(new_data, index)
        # print(new_data)
