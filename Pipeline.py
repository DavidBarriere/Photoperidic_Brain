import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'python3' ) )

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from CopyFileDirectoryRm import *
from DataRotation import *
from DataNormalization import *
from DataCropping import *
from DataBiasFieldCorrection import *
from DataFiltering import *

def runPipeline( Dir,
                 subjectJsonFileName,
                 taskJsonFileName,
                 verbose ):

  ##############################################################################
  # reading subject information
  ##############################################################################

    subjects = dict()
    with open( subjectJsonFileName, 'r' ) as f:
        subjects = json.load( f )

  ##############################################################################
  # reading task information
  ##############################################################################

    taskDescription = dict()
    with open( taskJsonFileName, 'r' ) as f:
        taskDescription = json.load( f )

  ##############################################################################
  # first loop over groups and individuals to perform individual processing
  ##############################################################################

    for subject in subjects.keys():

        print( "=====================================================" )
        print( subject + ' ' + "Prepare IR Data" )
        print( "=====================================================" )

        ########################################################################
        # Data Rotation
        ########################################################################

        if ( taskDescription[ "DataRotation" ] == 1 ):

            if ( verbose == True ):

            	runDataRotation( Dir,
		                           subject,
		                           1 )

        ########################################################################
        # Data Normalization
        ########################################################################

        if ( taskDescription[ "DataNormalization" ] == 1 ):

            if ( verbose == True ):

            	BrainTemplate = os.path.join( Dir,
                                          '00-DataSet',
                                          'Turone_Sheep_Brain_Template_And_Atlas',
                                          'Head_Templates',
                                          'head_ir_template.nii.gz ' ) 

            	runDataNormalization( Dir,
                                    subject,
                                    BrainTemplate,
                                    1 )

        ########################################################################
        # Data Cropping
        ########################################################################

        if ( taskDescription[ "DataCropping" ] == 1 ):

            if ( verbose == True ):

            	runDataCropping( Dir,
                               subject,
                               1 )

        ########################################################################
        # Data Bias Field Correction
        ########################################################################

        if ( taskDescription[ "DataBiasFieldCorrection" ] == 1 ):

            if ( verbose == True ):

            	runBiasFieldCorrection( Dir,
                                      subject,
                                      1 )

        ########################################################################
        # Data Non Local Means Filtering
        ########################################################################

        if ( taskDescription[ "DataFiltering" ] == 1 ):

            if ( verbose == True ):

            	runFiltering( Dir,
                            subject,
                            1 )
