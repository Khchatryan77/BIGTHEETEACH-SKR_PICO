from machine import UART, Pin
import time
from register import REGISTORS

time.sleep(8)
import _thread

FAN1 = Pin(17, Pin.OUT)

buffer = []

# UART1 on GPIO8 (TX) and GPIO9 (RX)
uart1 = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))  # 115200 is more typical

uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))  # 115200 is more typical

SLAVE_ADDR_1 = 0x00
SLAVE_ADDR_2 = 0x01
SLAVE_ADDR_3 = 0x02
SLAVE_ADDR_4 = 0x03

Motors = {
    "Motor_X":{
        "step_pin": Pin(11, Pin.OUT),
        "dir_pin": Pin(10, Pin.OUT),
        "en_pin": Pin(12, Pin.OUT),
        "End_stop_X": Pin(4, Pin.OUT)
    },
    "Motor_Y":{
        "step_pin": Pin(6, Pin.OUT),
        "dir_pin": Pin(5, Pin.OUT),
        "en_pin": Pin(7, Pin.OUT),
        "End_stop_Y": Pin(3, Pin.OUT)
    },
    "Motor_Z": {
        "step_pin": Pin(19, Pin.OUT),
        "dir_pin": Pin(28, Pin.OUT),
        "en_pin": Pin(2, Pin.OUT),
        "End_stop_Z": Pin(14, Pin.OUT)
    },
    "Motor_E": {
        "step_pin": Pin(14, Pin.OUT),
        "dir_pin": Pin(13, Pin.OUT),
        "en_pin": Pin(15, Pin.OUT),
        "End_stop_E": Pin(4, Pin.OUT)
    }
}

# Motors["Motor_X"]["step_pin"].on()
# Motors["Motor_X"]["dir_pin"].on()

Motors["Motor_X"]["en_pin"].on()
Motors["Motor_Y"]["en_pin"].on()
Motors["Motor_Z"]["en_pin"].on()

Running = True

def end_stop_handler(pin):
    global Running
    Running= False

Motors['Motor_X']['End_stop_X'].irq(trigger=Pin.IRQ_FALLING, handler=end_stop_handler)

def uart0_handler():
    if uart0.any():  # check if there is data
        data = uart0.read().decode().strip()  # read all available data
        buffer.append(data)
        print("Received:", data)
        return data

def move_steps(motor_step_pin, motor_dir_pin, motor_en_pin, steps, direction, delay_us=20):
    motor_dir_pin.value(direction)  # 0 or 1
    motor_en_pin.value(0)
    for _ in range(steps):
        motor_step_pin.high()
        time.sleep_us(delay_us)
        motor_step_pin.low()
        time.sleep_us(delay_us)
    motor_en_pin.value(1)

def move_steper_sync(motor_step_pin1, motor_dir_pin1, motor_en_pin1, motor_step_pin2, motor_dir_pin2, motor_en_pin2,  steps, direction, delay_us=20):
    motor_dir_pin1.value(direction)  # 0 or 1
    motor_en_pin1.value(0)
    motor_dir_pin2.value(direction)  # 0 or 1
    motor_en_pin2.value(0)
    for _ in range(steps):
        motor_step_pin2.high()
        motor_step_pin1.high()
        time.sleep_us(delay_us)
        motor_step_pin1.low()
        motor_step_pin2.low()
        time.sleep_us(delay_us)
    motor_en_pin1.value(1)
    motor_en_pin2.value(1)

def crc8(datagram, initial_value=0):
    crc = initial_value
    # Iterate bytes in data
    for byte in datagram:
         # Iterate bits in byte
        for _ in range(0, 8):
            if (crc >> 7) ^ (byte & 0x01):
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
            # Shift to next bit
            byte = byte >> 1
    return crc

def response_uart():
    if uart1.any():
        # R = uart.read()
        # print('R', R)
        for i in range(10):
            response = uart1.read(4)
            if response is not None and len(response) >= 2:
                if response[1] == 255:
                    response2 = uart1.read(4)
                    if response2 is not None:
                        print('response', response + response2)
                        if response[2] == REGISTORS['IFCNT']:
                            print('IFCNT', response2[2])
                    else:
                        pass
                        # print('response2 is None')
                else:
                    pass
                    # print('Its Echo')
            else:
                pass
                # print('response is None or too short')
    else:
         print("Invalid read response:")
    time.sleep_us(50)

def read_register(slave, reg):
    sync = 0x05
    addr = slave
    packet = [sync, addr, reg]
    crc = crc8(packet)
    uart1.write(bytearray(packet + [crc]))
    time.sleep_us(140)  #140

def write_register(slave, reg, value):
    sync = 0x05
    addr = slave
    reg_write = reg | 0x80

    data = [(value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF]


    packet = [sync, addr, reg_write] + data
    print('packet', packet)
    crc = crc8(packet)

    uart1.write(bytearray(packet + [crc]))
    time.sleep_us(500)

    response_uart()

def core_1():
    global Motors, uart0, buffer, Running

    while Running:
        if len(buffer) >= 1:
            move_steper_sync(Motors["Motor_Z"]["step_pin"], Motors["Motor_Z"]["dir_pin"], Motors["Motor_Z"]["en_pin"],
                                 Motors["Motor_E"]["step_pin"], Motors["Motor_E"]["dir_pin"], Motors["Motor_E"]["en_pin"], 16000, 1,100)

            buffer.pop(0)

write_register(SLAVE_ADDR_1, REGISTORS['GCONF'], 0b11001000)
write_register(SLAVE_ADDR_2, REGISTORS['GCONF'], 0b11001000)
write_register(SLAVE_ADDR_3, REGISTORS['GCONF'], 0b11001000)
write_register(SLAVE_ADDR_4, REGISTORS['GCONF'], 0b11001000)

write_register(SLAVE_ADDR_1, REGISTORS['CHOPCONF'], 0x15000053)
write_register(SLAVE_ADDR_2, REGISTORS['CHOPCONF'], 0x15000053)
write_register(SLAVE_ADDR_3, REGISTORS['CHOPCONF'], 0x15000053)
write_register(SLAVE_ADDR_4, REGISTORS['CHOPCONF'], 0x15000053)

FAN1.value(1)

_thread.start_new_thread(core_1,())

while Running:
    uart0_handler()
    if len(buffer) >= 1:
        # with lock:
        move_steper_sync(Motors["Motor_X"]["step_pin"], Motors["Motor_X"]["dir_pin"], Motors["Motor_X"]["en_pin"],
                             Motors["Motor_Y"]["step_pin"], Motors["Motor_Y"]["dir_pin"],Motors["Motor_Y"]["en_pin"],16000, 1, 100)

    #print('buffer', buffer)
    print(Motors['Motor_X']['End_stop_X'].value())
    if Motors['Motor_X']['End_stop_X'].value() == 0:
        break

    # read_register(SLAVE_ADDR_1, REGISTORS["IFCNT"])
    # time.sleep(0.01)
    # response_uart()
