import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'python3' ) )

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from CopyFileDirectoryRm import *
from DataVisualization import *

def runPipeline( Dir,
                 taskJsonFileName,
                 verbose ):

  ##############################################################################
  # reading task information
  ##############################################################################

    taskDescription = dict()
    with open( taskJsonFileName, 'r' ) as f:
        taskDescription = json.load( f )


	########################################################################
	# Data Visualization
	########################################################################

    if ( taskDescription[ "DataVisualization" ] == 1 ):
    	if ( verbose == True ):
    		runDataVisualization( Dir,
    				      1 )
