import time
import board
import busio
import digitalio
import adafruit_bmp280

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO = board.MISO)
cs = digitalio.DigitalInOut(board.D5)
bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, cs)

bmp280.sea_level_pressure = 1011.7

while True:
	#print(f'tempeessure)
	print("altitued : ",bmp280.altitude)
	print("temperature :", bmp280.temperature)
	time.sleep(0.5)
