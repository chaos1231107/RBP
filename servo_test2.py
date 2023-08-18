
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

try:
    pwm.ChangeDutyCycle(12.5)  # 180도에 해당하는 듀티 사이클 (12.5%)
    time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()