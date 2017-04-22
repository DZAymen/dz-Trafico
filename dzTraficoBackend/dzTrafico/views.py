from django.http import HttpResponse
from django.shortcuts import render
import traci as tr
# Create your views here.
def home(request):
    tr.start(["sumo", "-c", "F:/PFE/Realisation/study-case/map.sumocfg"])
    tr.simulationStep()
    speed = tr.inductionloop.getLastStepMeanSpeed("1")
    #return HttpResponse("This is the home page")
    tr.close()
    return HttpResponse(speed)