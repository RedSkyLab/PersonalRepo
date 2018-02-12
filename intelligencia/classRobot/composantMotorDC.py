from . import export
import RPi.GPIO as GPIO
from time import sleep
import asyncio

@export
class MotorDC:
    RequiredElements = ['Type','NumberPorts','Utilisation','PortNames']
    def __init__(self,Configuration):
        for conf in self.RequiredElements:
            if(conf not in Configuration.keys()):
                print('Error')
                assert Exception
        self.Type = Configuration['Type']
        self.NumberOfPorts = Configuration['NumberPorts']
        if(isinstance(Configuration, list)):
            for port in Configuration['PortNames']:
                Query = "self."+port + " = " + Configuration[port]
                exec(Query)
        else:
            Query = "self." + Configuration['PortNames'] + " = " + Configuration[Configuration['PortNames']]
            exec(Query)
            
        self.Settle = 0

    ## Controle d'un moteur DC par le Raspberry Pi

        GPIO.setmode(GPIO.BCM)              # GPIO Numbering

        GPIO.setup(self.PWM, GPIO.OUT)

 

    async def SetAngle(self, angle,nbrTour,Sleep):
        GPIO.setmode(GPIO.BCM)              # GPIO Numbering

        GPIO.setup(self.PWM, GPIO.OUT)
        print('Start Turning')
   # pin 17 à 50Hz
        pwm=GPIO.PWM(self.PWM,100)
        pwm.start(5)

        angle1 = 0
        duty1 = float(angle1)/10 + 5

        angle2=angle
        duty2= float(angle2)/10 + 5

        i = 0

        while i < nbrTour:
            if(self.Settle == duty2):
                pwm.ChangeDutyCycle(duty1)
                sleep(0.8)
                self.Settle = duty1
            else:
                pwm.ChangeDutyCycle(duty2)
                sleep(0.8)
                self.Settle = duty2
            
            i = i+1
        GPIO.cleanup()
        
        await asyncio.sleep(Sleep)

        pwm.stop()
        print('StopTurning')
        return 'Turned'


