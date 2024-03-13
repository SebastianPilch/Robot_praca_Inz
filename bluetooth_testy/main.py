import Controller_state as Cs
import time
from threading import Thread
import Motors_control as Mt
import subprocess
import Shear_memory_C as mem
import PCA_communication as comm
global ps4


#wyszukaj pada
def connection_control():
    global ps4
    while True:
        result = subprocess.run(['bluetoothctl','devices'], capture_output=True)
        out =  str(result.stdout)[9:26]
        if out != 'A0:5A:5D:5B:6A:72':
            set_connection()


        time.sleep(10)

def set_connection():
    connection_refused = True
    while connection_refused:
        result = subprocess.run(['bluetoothctl','connect','A0:5A:5D:5B:6A:72'], capture_output=True)
        out_info = str(result.stdout).split('\\n')[1][:7]
        print(out_info)
        if out_info == "Connect":
            connection_refused = False


    return True

def C_thread():
    subprocess.run("echo orangepi | sudo -S -s /home/orangepi/Desktop/Sterowanie_serwa_PWM/PWM_control/main",shell = True,check = True)
def ds4drv():
    subprocess.run("echo orangepi | sudo -S -s ds4drv",shell = True,check = True )
    



ds4drv_th = Thread(target=ds4drv)
ds4drv_th.start()
print("sterowniki uruchomione")
time.sleep(4)

set_connection()
# # time.sleep(5)
# #ustaw diody kontrolne do aktywnego silnika
result = subprocess.run(['gpio','mode','6','OUT'], capture_output=True)
result = subprocess.run(['gpio','mode','9','OUT'], capture_output=True)
result = subprocess.run(['gpio','mode','10','OUT'], capture_output=True)
result = subprocess.run(['gpio','mode','13','OUT'], capture_output=True)
result = subprocess.run(['gpio','mode','15','OUT'], capture_output=True)

ps4 = Cs.PS4Controller()
ps4.init()



mem.create_mem()
# uruchomienie_c_po_sudo = Thread(target=C_thread)
# uruchomienie_c_po_sudo.start()
print("watek c uruchomiony")

Controller_thread = Thread(target=connection_control)
Controller_thread.start()
Controller_thread = Thread(target=ps4.listen)
Controller_thread.start()
time.sleep(0.5)
Controller_thread = Thread(target=Mt.Buttons_axis,args=[ps4])
Controller_thread.start()
Controller_thread = Thread(target=comm.Servo_control)
Controller_thread.start()
