import mmap
import ctypes
import struct
# Definicja struktury z 6 polami typu int
class PWM_stepper(ctypes.Structure):
    _fields_ = [
        ("width_arm", ctypes.c_int),
        ("width_hand", ctypes.c_int),
        ("width_manipulator_rotation", ctypes.c_int),
        ("width_manipulator", ctypes.c_int),
        ("do_step", ctypes.c_int),
        ("direction", ctypes.c_int),
        ("step_speed", ctypes.c_int)
    ]



    def __str__(self):
        return f"{self.width_arm}, {self.width_hand}, {self.width_manipulator_rotation}, {self.width_manipulator}, {self.do_step}, {self.direction}, {self.step_speed} /n"

# Tworzenie pamięci współdzielonej      00                                                                                                                                                                                                              
def create_mem():
    with open("../PWM_and_stepper_data.bin", "wb") as file:
        file.write(b'\0' * mmap.PAGESIZE)  # Zapewnienie odpowiedniego rozmiaru


# Uzyskiwanie dostępu do pamięci współdzielonej
def mem_access():
    with open("../PWM_and_stepper_data.bin", "r+b") as file:
        shared_memory = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_WRITE)

        # Tworzenie obiektu klasy WspoldzielonaStruktura na podstawie pamięci współdzielonej
        return PWM_stepper.from_buffer(shared_memory)

    

# Przykładowe użycie

# Utwórz pamięć współdzieloną (możesz to zrobić tylko raz)

def update_position(new_posiotion_data):
    data_structure = mem_access()
    # print(data_structure)
    if new_posiotion_data[1]<2500:
        if new_posiotion_data[1]> 500:
            data_structure.width_arm = int(new_posiotion_data[1])
        else:
            data_structure.width_arm = 500
    else:
        data_structure.width_arm = 2500

    if new_posiotion_data[2]<2500:
        if new_posiotion_data[2]> 500:
            data_structure.width_hand = int(new_posiotion_data[2])
        else:
            data_structure.width_hand = 500
    else:
        data_structure.width_hand = 2500

    if new_posiotion_data[3]<2450:
        if new_posiotion_data[3]> 500:
            data_structure.width_manipulator_rotation = int(new_posiotion_data[3])
        else:
            data_structure.width_manipulator_rotation = 500
    else:
        data_structure.width_manipulator_rotation = 2450

    if new_posiotion_data[4]<2450:
        if new_posiotion_data[4]> 500:
            data_structure.width_manipulator = int(new_posiotion_data[4])
        else:
            data_structure.width_manipulator = 500
    else:
        data_structure.width_manipulator = 2450
 
    data_structure.do_step = new_posiotion_data[0]
    data_structure.direction = new_posiotion_data[5] 
    data_structure.step_speed = int(new_posiotion_data[6])
    # struct_size = struct.calcsize((PWM_stepper._type_))
    # print(data_structure)
    with open("../PWM_and_stepper_data.bin","r+b") as file:
        with mmap.mmap(file.fileno(),0,access=mmap.ACCESS_WRITE) as shared_memory:
            shared_memory.write(data_structure)
            shared_memory.flush()
            # print(shared_memory.readline())
            
            # file.close()

    file.close()
# create_mem()
# update_position([2500,750,3,4,12,6,700])
# print(mem_access())