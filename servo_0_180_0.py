import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setwarnings(False)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

try:
    pwm.ChangeDutyCycle(12.5)  # 12.5 means 180 degrees
    time.sleep(1)  # program waits for 1 second
    pwm.ChangeDutyCycle(2.5)  # Change to 0 degrees (0.5ms pulse width)
    time.sleep(0.5)  # program waits for 0.7 second

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
