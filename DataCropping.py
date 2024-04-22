import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'python' ) )

from CopyFileDirectoryRm import *

def runDataCropping( Dir,
                     subject,
                     verbose ):
                      
  
	if ( verbose == True ):

	#-----------------------------------------------------------------------------
	# Make Directories
	#-----------------------------------------------------------------------------

		makedir( os.path.join( Dir,
	                              '01-PrepareData',
	                              '03-Cropping' ) )

	#-----------------------------------------------------------------------------
	# Data Cropping
	#-----------------------------------------------------------------------------

		for i in range(1, 3, 1):
			session = 'ses-' + str(i)
			
			print ( '    #-----------------------------------------------' )
			print ( '    # Cropping of ' + subject + '_' + session + ' IR data' )
			print ( '    #-----------------------------------------------' )

			command = 'AimsSubVolume ' + \
			'-i ' + os.path.join( Dir,
					       '01-PrepareData',
					       '02-Normalization',
					       subject + '_' + session + '.nii.gz ' ) + \
			'-o ' + os.path.join( Dir,
					       '01-PrepareData',
					       '03-Cropping',
					       subject + '_' + session + '.nii.gz ') + \
			'-x 74 ' + \
			'-X 213 ' + \
			'-y 104 ' + \
			'-Y 313 ' + \
			'-z 40 ' + \
			'-Z 201'

			os.system( command )

			command = 'rm -f ' + \
				  os.path.join( Dir,
						'01-PrepareData',
						'03-Cropping',
						subject + '_' + session + '.nii.gz.minf ')
			os.system( command )

