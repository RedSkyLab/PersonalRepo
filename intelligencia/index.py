"""
Controller Robot Test Example
 Dans cette fonction on retrouve la complete manipulation de la classe Robot
 par les differents types de besoin pour le programme
 Liste de besoins:
 -Exercice Entrainement With Strike : ExerciceWithStrike
 -Robot Training with SparBar : RobotTrainSparbar
 -Robot training normal : RobotTrain
 -Main Menu IU Utilisateur: Main
 Ces besoins seront lances en paralleles et diriges par ce controlleur pour modeliser les differentes actions:

dfsd
"""
#Constantes Parametriques
CONST_FILE_ROBOT = "Robot.aee"

#Implementation des Modules et Librairies Python
import re
import asyncio
import time
import RPi.GPIO as GPIO

#Implementation du des differents composants
from classRobot import *
import classBD as BD
import classMoyenne as Moyenne
import classTimer as Timer
import classExercice as Exercice
import classCoup as Coup



class ControllerRobot:
    #Ports du robot qui seront transmis a la classe robot
    Robot = {}
    #Modules Installes du Robot
    RobotModules = {}

    InstalledModules = {'Ultrasonic','MotorDC'}

    def __init__(self, sControllerType,aParams = []):
        self.RobotModules = self.obtainRobotCaractersModules(CONST_FILE_ROBOT)
        self.Robot = self.recognizeTypes()
        self.Tasks = []
        if (sControllerType == "ExerciceWithStrike"):
            self.controllerExerciceWithStrike(aParams)
        elif (sControllerType == "RobotTrainSparbar"):
            self.controllerRobotTrainSparbar(aParams)
        elif (sControllerType == "RobotTrain"):
            self.controllerRobotTrain(aParams)
        elif (sControllerType == "Main"):
            self.controllerMain(aParams)
        else:
            #Remplace par module Error Not Train
            print("Error")
        return

    def recognizeTypes(self):
        Temporal = {}
        if(self.InstalledModules == {}):
            #Remplacer par module Error Not Installed
            print('Is not installed')
            return
        for element in self.RobotModules.keys():
            if(self.RobotModules[element]['Type']):
                if(self.getConfMod(element,'Type') in self.InstalledModules):
                    Temporal[element] = eval(self.getConfMod(element,'Type')+"("+str(self.getConfMod(element))+")")
                else:
                    #Remplacer par module Error Type not installed
                    print('Module Type is Not Installed')
            else:
                #Remplacer par module Error No Type 
                print('Module Has No Type')
        return Temporal


    def controllerMain(self, aParams): return
    def controllerRobotTrain(self, aParams): return
    def controllerRobotTrainSparbar(self, aParams): return
    def controllerExerciceWithStrike(self, aParams): return
    def obtainRobotCaractersModules(self,sFile):
        ObjectsRegex = re.compile('Objects ?= ?/(.+?)/')
        file = open(sFile,'r').read()
        MatchesObjects = ObjectsRegex.match(file).groups(0)[0].split(',')
        DictRegex = {}
        ReturnReg = {}
        for match in MatchesObjects:
            DictRegex[match] = re.compile(r"<" + match + ">(.+?)<End" + match + ">")

        for Object in DictRegex.keys():
            if(DictRegex[Object].search(file) == None):
                #Remplace par Module erreur
                print(Object + 'Error')
            else:
                DictRegex[Object]= DictRegex[Object].search(file).groups(0)[0].strip().split(';')
                ReturnReg[Object] = {}
                for Caracteristique in DictRegex[Object]:
                    temporalVar = Caracteristique.split('=')
                    """print(temporalVar[1])"""
                    if(',' in temporalVar[1]):
                    
                        ReturnReg[Object][temporalVar[0].strip()] = temporalVar[1].strip().split(',')
                    else:
                        ReturnReg[Object][temporalVar[0].strip()] = temporalVar[1].strip()

        return ReturnReg
    def getConfMod(self,Mod,Char=''):
        if(Mod not in self.RobotModules):
            #Module Dont exist Remplace Error
            print("Error")
            return
        else:
            if(Char == ''):
                return self.RobotModules[Mod]
            else:
                return self.RobotModules[Mod][Char]
    def displayModulesPrint(self):
        for material in self.RobotModules.keys():
            print("MATERIAL :" + material)
            for Specs in robot.RobotModules[material].keys():
                print(Specs+ " :: "+ str(robot.RobotModules[material][Specs]))
            print("\n")
    async def useModule(self,Mod,Method = "run",Requests = 1,Sleep = 0, aParams=[]):
        tasks = []
        if(Mod not in self.Robot.keys()):
            #Module Dont exist Remplace Error
            print("Error")
        else:
            if(Method in dir(self.Robot[Mod])):
                sParams = str(aParams).strip("[")
                sParams = sParams.strip("]")

                for idx in range(1, Requests+1):
                    Query = "self.Robot['" + Mod + "']." + Method + "(" + sParams + ")"
                    tsk = asyncio.ensure_future(eval(Query))
                    self.Tasks.append(tsk)
                    asyncio.sleep(Sleep)

            else:
                #Replace for Module Error, Method Composant Dont Exist
                print("Error h")

    def run(self):
        Loop = asyncio.get_event_loop()
        Loop.run_until_complete(asyncio.gather(*self.Tasks))
        self.Tasks = []
    async def _do(self, Funcs = []):
        await asyncio.wait(Funcs)

    def do(self,Funcs = []):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._do(Funcs))
        except Exception:
            #Remplace error Execution not possible
            print("Error")
            return
        robot.run()




robot = ControllerRobot('Main')

robot.do(
    [
	robot.useModule('UltrasonGaucheTorse','mesureForce',1,0,[1])
    ]
)
robot.Robot['UltrasonGaucheTorse'].DisplayMax()





