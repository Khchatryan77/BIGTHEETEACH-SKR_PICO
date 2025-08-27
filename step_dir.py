from machine import UART, Pin
import time

# UART1 on GPIO8 (TX) and GPIO9 (RX)
# uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))  # 115200 is more typical

End_stop1 = Pin(4, Pin.IN, Pin.PULL_UP)


step_pin = Pin(11, Pin.OUT)
dir_pin = Pin(10, Pin.OUT)
en_pin = Pin(12, Pin.OUT)

step_pin_z = Pin(14, Pin.OUT)
dir_pin_z = Pin(13, Pin.OUT)
en_pin_z = Pin(15, Pin.OUT)

step_pin_y = Pin(6, Pin.OUT)
dir_pin_y = Pin(5, Pin.OUT)
en_pin_y = Pin(7, Pin.OUT)


en_pin.value(0)
en_pin_y.value(0)
en_pin_z.value(0)

def move_steps(steps, direction, delay_us=20):
    dir_pin.value(direction)  # 0 or 1
    for _ in range(steps):
        step_pin.high()
        time.sleep_us(delay_us)
        step_pin.low()
        time.sleep_us(delay_us)

def move_steps_y(steps, direction, delay_us=20):
    dir_pin_y.value(direction)  # 0 or 1
    for _ in range(steps):
        step_pin_y.high()
        time.sleep_us(delay_us)
        step_pin_y.low()
        time.sleep_us(delay_us)

def move_steps_z(steps, direction, delay_us=20):
    dir_pin_z.value(direction)  # 0 or 1
    for _ in range(steps):
        step_pin_z.high()
        time.sleep_us(delay_us)
        step_pin_z.low()
        time.sleep_us(delay_us)


while True:
    move_steps(3200,1,50)
    move_steps_y(3200, 1, 50)
    move_steps_z(3200, 1, 50)
    print('motor first moved')
    time.sleep(1)
    move_steps(3200,0,50)
    move_steps_y(3200, 0, 50)
    move_steps_z(3200, 0, 100)
    print('motor second moved')
    time.sleep(1)

    # print(f'end_stop_1== {End_stop1.value()}')
    # time.sleep_ms(200)