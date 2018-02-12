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
        # On utilise un setup GPIO en BCM
        # ce qui permet d'utiliser les numéros physiques des broches
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # On définit les pins en entrée et en sortie
        GPIO.setup(self.Trigg,GPIO.OUT)  # Trigger
        GPIO.setup(self.Echo,GPIO.IN)    # Echo

    async def mesureForce(self, pause):

        # On place le trigger en false (Low)
        GPIO.output(self.Trigg, False)

        # On permet une pause du module entre différentes mesures
        time.sleep(pause)

        # on envoie des impulsions de 10µs
        GPIO.output(self.Trigg, True)
        time.sleep(pause)
        GPIO.output(self.Trigg, False)
        start = time.time()
        while GPIO.input(self.Echo)==0:
          start = time.time()

        while GPIO.input(self.Echo)==1:
          stop = time.time()

        #On prend le temps qu'a pris le son pour faire l'aller retour
        TempsAllerRetour = stop-start

        #On multiplie le temps obtenu par la vitesse du son en cm/s
        distance = TempsAllerRetour * 17150

        print("Distance {}".format(distance))

        #partie pour prendre la force à partir de la distance
        distanceInit = 12
        distanceParcourue = distanceInit - distance
        print("La distance parcourue est de : {} cm".format(distanceParcourue))
        # K = 3.913N/mm soit 39.13N/cm => distance en cm donc conversion de K
        # Autre méthode est de faire 3.913 * distanceParcourue 
        force = (39.13 * distanceParcourue)
        print("La force du coup est de : {} N".format(force))

        #On met dans une liste les différentes mesures de force       
        self.ListTest.append(force)

        await asyncio.sleep(pause)
        return 'Mesure Token'




    def DisplayMax(self):
       print(max(self.ListTest))