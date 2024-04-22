import os, json, sys


from Pipeline import *

Dir = '/home/dbarriere/Recherche/PhotoperiodicBrain/Analysis'
subjectJsonFileName = os.path.join( Dir,
                                    'subjects.json' )
taskJsonFileName = os.path.join( Dir,
                                 'TaskJsonFileName.json' )
verbose = 1
runPipeline( Dir,
             subjectJsonFileName,
             taskJsonFileName,
             verbose )
