import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

class AnalogIntensity:
	"""
	Aids in reading voltage outputs in each of the pins
	"""
	def __init__(self):
		self.intens_pin = "P8_7"
		self.voltage = 0
		ADC.setup()

	def get_intensity(self):
		tot_intensity = 0
		for i in range(0, 100):
			value = ADC.read(intens_pin) #insert port name 
			value = ADC.read(intens_pin) #read value twice, because of a bug
			value = value * voltage
			tot += value
		avg_intensity = tot / 100
		print("intensity: ", avg_intensity)

	def test_port(self):
		print(ADC.read("P9_33")) #0.663736283779
		print(ADC.read("P9_35")) #0.408791214228
		print(ADC.read("P9_36")) #0.626129448414
		print(ADC.read("P9_37")) #0.927960932255
		print(ADC.read("P9_38")) #0.577777802944
		print(ADC.read("P9_39")) #0.913308918476
		print(ADC.read("P9_40")) #0.827106237411