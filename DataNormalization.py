import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'python' ) )

from CopyFileDirectoryRm import *

def runDataNormalization( Dir,
                          subject,
                          BrainTemplate,
                          verbose ):
                      
  
	if ( verbose == True ):

	#-----------------------------------------------------------------------------
	# Make Directories
	#-----------------------------------------------------------------------------

		makedir( os.path.join( Dir,
	                              '01-PrepareData',
	                              '02-Normalization' ) )

	#-----------------------------------------------------------------------------
	# Data Normalization
	#-----------------------------------------------------------------------------

		for i in range(1, 3, 1):
			session = 'ses-' + str(i)
			
			print ( '    #-----------------------------------------------' )
			print ( '    # Normalization of ' + subject + '_' + session + ' IR data' )
			print ( '    #-----------------------------------------------' )

			command = 'antsRegistrationSyNQuick.sh ' + \
			          '-d 3 ' + \
			          '-f ' + BrainTemplate + \
			          ' -m ' + os.path.join( Dir,
						        '01-PrepareData',
						        '01-Rotation',
						        subject + '_' + session + '.nii.gz ' ) + \
			          '-o ' + os.path.join( Dir,
					       	 '01-PrepareData',
					       	 '02-Normalization',
					                 subject + '_' + session + '_ ' ) + \
			          '-t a '

			os.system( command )

			command = 'rm -f ' + \
				  os.path.join( Dir,
						'01-PrepareData',
						'02-Normalization',
						subject + '_' + session + '_Warped.nii.gz ' ) + \
				  os.path.join( Dir,
						'01-PrepareData',
						'02-Normalization',
						subject + '_' + session + '_InverseWarped.nii.gz ' )
			os.system( command )

			command = 'antsApplyTransforms ' + \
			          '-d 3 ' + \
			          '-e 0 ' + \
			          '-i ' + os.path.join( Dir,
						        '01-PrepareData',
						        '01-Rotation',
						        subject + '_' + session + '.nii.gz ' ) + \
				  '-o ' + os.path.join( Dir,
						        '01-PrepareData',
						        '02-Normalization',
						        subject + '_' + session + '.nii.gz ' ) + \
				  '-r ' + BrainTemplate + \
				  ' -n Linear ' + \
				  '-t ' + os.path.join( Dir,
						        '01-PrepareData',
						        '02-Normalization',
						        subject + '_' + session + '_0GenericAffine.mat' )

			os.system( command )

