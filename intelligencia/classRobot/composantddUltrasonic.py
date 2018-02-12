from . import export
import RPi.GPIO as GPIO
import time
import asyncio



@export

class Ultrasonic:
    ValuesCharge = {}
    ListTest = []
    RequiredElements = ['Type','NumberPorts','Utilisation','PortNames']
    def __init__(self,Configuration):
        for conf in self.RequiredElements:
            if(conf not in Configuration.keys()):
                print('Error')
                assert Exception
        self.Type = Configuration['Type']
        self.NumberOfPorts = Configuration['NumberPorts']
        for port in Configuration['PortNames']:
            Query = "self."+port + " = " + Configuration[port]
            exec(Query)

        ###SETUP OF ULTRASONIC MODULE###
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

    
        # Set pins as output and input
        GPIO.setup(self.Trigg,GPIO.OUT)  # Trigger
        GPIO.setup(self.Echo,GPIO.IN)    # Echo

    async def mesureForce(self, pause):

        # Set trigger to False (Low)
        GPIO.output(self.Trigg, False)

        # Allow module to settle
        time.sleep(pause)

        # Send 10us pulse to trigger
        GPIO.output(self.Trigg, True)
        time.sleep(pause)
        GPIO.output(self.Trigg, False)
        start = time.time()
        while GPIO.input(self.Echo)==0:
          start = time.time()

        while GPIO.input(self.Echo)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000

        # That was the distance there and back so halve the value
        distance = distance / 2

        #partie pour prendre la force à partir de la distance
        distanceInit = 12
        distanceParcourue = distanceInit - distance
        force = 3.913 * distanceParcourue
        
        self.ListTest.append(force)

        await asyncio.sleep(pause)
        return 'Mesure Token'
    def DisplayMax(self):
        print(max(self.ListTest))
        return