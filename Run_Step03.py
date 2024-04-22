import os, json, sys


from Pipeline_DataVisualization import *

Dir = '/home/dbarriere/Recherche/PhotoperiodicBrain/Analysis'

taskJsonFileName = os.path.join( Dir,
                                 'TaskJsonFileName_Step03.json' )
verbose = 1
runPipeline( Dir,
             taskJsonFileName,
             verbose )
