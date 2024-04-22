import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'python' ) )

from CopyFileDirectoryRm import *

def runDataRotation( Dir,
                     subject,
                     verbose ):
                      
  
	if ( verbose == True ):

	#-----------------------------------------------------------------------------
	# Make Directories
	#-----------------------------------------------------------------------------

		makedir( os.path.join( Dir,
	                              '01-PrepareData',
	                              '01-Rotation' ) )

	#-----------------------------------------------------------------------------
	# Data Rotation
	#-----------------------------------------------------------------------------

		for i in range(1, 3, 1):
			session = 'ses-' + str(i)
			
			print ( '    #-----------------------------------------------' )
			print ( '    # Rotation of ' + subject + '_' + session + ' IR data' )
			print ( '    #-----------------------------------------------' )
		    	
			command = 'AimsFlip ' + \
				  '-i ' + os.path.join( Dir,
						       '00-DataSet',
						        subject,
						        session,
						       'anat',
						       subject + '_' + session + '_inv-380_IRT1.nii.gz ') + \
				  '-o ' + os.path.join( Dir,
						        '01-PrepareData',
						        '01-Rotation',
						        subject + '_' + session + '.nii.gz ') + \
				  '-m YZ'

			os.system( command )

			command = 'rm -f ' + \
				  os.path.join( Dir,
						'01-PrepareData',
						'01-Rotation',
						subject + '_' + session + '.nii.gz.minf ')
			os.system( command )

			command = 'AimsFlip ' + \
				  '-i '  + os.path.join( Dir,
						        '01-PrepareData',
						        '01-Rotation',
						        subject + '_' + session + '.nii.gz ') + \
				  '-o ' + os.path.join( Dir,
						        '01-PrepareData',
						        '01-Rotation',
						        subject + '_' + session + '.nii.gz ') + \
				  '-m ZZ'

			os.system( command )

			command = 'rm -f ' + \
				  os.path.join( Dir,
						'01-PrepareData',
						'01-Rotation',
						subject + '_' + session + '.nii.gz.minf ')
			os.system( command )


