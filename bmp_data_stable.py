import time
import board
import busio
import digitalio
import adafruit_bmp280
import RPi.GPIO as GPIO

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, cs)
bmp280.sea_level_pressure = 1013.25
GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setwarnings(False)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

while True:
    altitude = bmp280.altitude
    temperature = bmp280.temperature
    print("Altitude: ", altitude)
    # file append mode 
    with open('bmp_data.txt', 'a') as file:
        file.write(f"Altitude: {altitude} m\n")
        file.flush()
        time.sleep(0.1)
        if altitude >= 3000:
            continue
    if altitude >= 95.5:
        try:
            pwm.ChangeDutyCycle(12.5)  # 12.5 means 180 degrees
            time.sleep(1)  # program waits for 1 second
            pwm.ChangeDutyCycle(2.5)  # Change to 0 degrees (0.5ms pulse width)
            time.sleep(0.7)  # program waits for 0.7 second
        except KeyboardInterrupt:
            pass
        #finally:
            #pwm.stop()
            #PIO.cleanup()
