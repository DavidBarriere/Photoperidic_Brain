import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'python' ) )

from CopyFileDirectoryRm import *

def runBiasFieldCorrection( Dir,
                            subject,
                            verbose ):
                      
  
	if ( verbose == True ):

	#-----------------------------------------------------------------------------
	# Make Directories
	#-----------------------------------------------------------------------------

		makedir( os.path.join( Dir,
	                              '01-PrepareData',
	                              '04-N4BiasFieldCorrection' ) )
	                              
	#-----------------------------------------------------------------------------
	# Bias Field Correction
	#-----------------------------------------------------------------------------

		for i in range(1, 3, 1):
			session = 'ses-' + str(i)
			
			print ( '    #-----------------------------------------------' )
			print ( '    # Bias Field Correction of ' + subject + '_' + session + ' IR data' )
			print ( '    #-----------------------------------------------' )

			command = 'ThresholdImage ' + \
                                 '3 ' + \
                                 os.path.join( Dir,
					        '01-PrepareData',
					        '03-Cropping',
					        subject + '_' + session + '.nii.gz ') + \
                                 os.path.join( Dir,
					        '01-PrepareData',
					        '04-N4BiasFieldCorrection',
					        subject + '_' + session + '_Otsu.nii.gz ' ) + \
                                 'Otsu 4'
			
			os.system( command ) 

			command = 'ThresholdImage ' + \
                                 '3 ' + \
                                 os.path.join( Dir,
					        '01-PrepareData',
					        '04-N4BiasFieldCorrection',
					        subject + '_' + session + '_Otsu.nii.gz ' ) + \
                                 os.path.join( Dir,
					        '01-PrepareData',
					        '04-N4BiasFieldCorrection',
					        subject + '_' + session + '_Otsu.nii.gz ' ) + \
                                 '1 Inf 1 0'
			os.system( command )

			command = 'ImageMath ' + \
                                 '3 ' + \
                                 os.path.join( Dir,
					        '01-PrepareData',
					        '04-N4BiasFieldCorrection',
					        subject + '_' + session + '_Otsu.nii.gz ' ) + \
                                 'GetLargestComponent ' + \
                                 os.path.join( Dir,
					        '01-PrepareData',
					        '04-N4BiasFieldCorrection',
					        subject + '_' + session + '_Otsu.nii.gz ' )
			os.system( command )

			command = 'N4BiasFieldCorrection ' + \
                                 '-d 3 ' + \
                                 '-s 4 ' + \
                                 '-b [ 200 ] ' + \
                                 '-c [ 50x50x50x50,0.0 ] ' + \
                                 '-w ' + os.path.join( Dir,
					                '01-PrepareData',
					                '04-N4BiasFieldCorrection',
					                subject + '_' + session + '_Otsu.nii.gz ' ) + \
                                 '-i ' + os.path.join( Dir,
					                '01-PrepareData',
					                '03-Cropping',
					                subject + '_' + session + '.nii.gz ') + \
                                 '-o ' + os.path.join( Dir,
					                '01-PrepareData',
					                '04-N4BiasFieldCorrection',
					                subject + '_' + session + '.nii.gz ' )

			os.system( command )
