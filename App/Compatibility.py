# Import required Python libraries
import time
import RPi.GPIO as GPIO


#Constantes globale
DEFINED_DISTANCE = 8.8
DEFINED_COEF = 3.913
MODE_DEVELOPPEMENT = False




# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

print("Ultrasonic Measurement")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

def obtainValues():
	global DEFINED_DISTANCE, DEFINED_COEF, MODE_DEVELOPPEMENT
	# Set trigger to False (Low)
	GPIO.output(GPIO_TRIGGER, False)

	# Allow module to settle
	time.sleep(0.02)

	# Send 10us pulse to trigger
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	start = time.time()
	while GPIO.input(GPIO_ECHO)==0:
	  start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
	  stop = time.time()

	# Calculate pulse length
	elapsed = stop-start

	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	distance = elapsed * 34000

	# That was the distance there and back so halve the value
	distance = distance / 2

	print("Distance : %.1f" % distance)
	if(MODE_DEVELOPPEMENT):
		power = (DEFINED_DISTANCE - distance)* DEFINED_COEF
		if(power<0):
			print("INFINI")
		else:
			print("Power : {0}".format(power))
		return distance,power

	# Reset GPIO settings
	
	return distance


print("Force est de {}".format(obtainValues()))
	
	
	
	
	
	

	
GPIO.cleanup()
