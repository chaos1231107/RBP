import time
import board
import busio
import digitalio
import adafruit_bmp280
import RPi.GPIO as GPIO
import numpy as np

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, cs)
bmp280.sea_level_pressure = 1013.25

GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def moving_average(data, window):
    moving_avg = []
    for i in range(len(data)):
        if i < window:
            moving_avg.append(data[i])
        else:
            partial_avg = np.mean(data[i - window + 1 : i + 1])
            moving_avg.append(partial_avg)
    return moving_avg

window = 3
data = []
moving_std = []
alpha = 0.25
beta = 0.125
temp_altitude = []
init_altitude = 0  

while True:
    altitude = bmp280.altitude
    if init_altitude == 0:
        init_altitude = altitude
    
    cali_altitude = altitude - init_altitude
    result = cali_altitude
    data.append(result)

    if len(data) < window:
        data.append(init_altitude)
    
    ma = moving_average(data, window)
    ma = np.array(ma)

    estimated = ma[-1]
    estimated = (1 - alpha) * estimated + alpha * result
    var = np.var(data[-window:])
    var = (1 - beta) * var + beta * abs(result - estimated)
    
    print("Initial Altitude: ", init_altitude)
    print("Real Altitude: ", altitude)
    print("Moving Average: ", estimated)
    print("Calibration Altitude: ", cali_altitude)
    
    if cali_altitude >= 0.5:
        try:
            pwm.ChangeDutyCycle(12.5)
            time.sleep(1)
            pwm.ChangeDutyCycle(2.5)
            time.sleep(0.7)
        except KeyboardInterrupt:
            pass
    
    if not abs(cali_altitude - estimated) <= np.sqrt(var):
        pwm.ChangeDutyCycle(0)
        init_altitude = 0
    
    with open('log_data.txt', 'a') as file:
        file.write(f'Calibration Altitude: {cali_altitude} m\n')
        file.flush()
        time.sleep(0.1)
    
    time.sleep(0.3)

