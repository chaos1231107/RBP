import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

pwm.ChangeDutyCycle(3.0)
time.sleep(0.5)

pwm.ChangeDutyCycle(12.5)


pwm.stop()
pwm.cleanup()
