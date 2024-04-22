import os, json, sys, shutil
sys.path.insert( 0, os.path.join( os.sep, 'usr', 'share', 'gkg', 'python' ) )

from CopyFileDirectoryRm import *

def runFiltering( Dir,
                  subject,
                  verbose ):
                      
  
	if ( verbose == True ):

	#-----------------------------------------------------------------------------
	# Make Directories
	#-----------------------------------------------------------------------------

		makedir( os.path.join( Dir,
	                              '01-PrepareData',
	                              '05-NonLocalMeansFiltering' ) )

	#-----------------------------------------------------------------------------
	# Bias Field Correction
	#-----------------------------------------------------------------------------

		for i in range(1, 3, 1):
			session = 'ses-' + str(i)
			
			print ( '    #-----------------------------------------------' )
			print ( '    # Non Local Means Filtering ' + subject + '_' + session + ' IR data' )
			print ( '    #-----------------------------------------------' )

			command = 'GkgExecuteCommand NonLocalMeansFilter ' + \
                                 '-i '  + os.path.join( Dir,
					                '01-PrepareData',
					                '04-N4BiasFieldCorrection',
					                subject + '_' + session + '.nii.gz ' ) + \
                                 '-o '  + os.path.join( Dir,
					                '01-PrepareData',
					                '05-NonLocalMeansFiltering',
					                subject + '_' + session + '.nii ' ) + \
                                 '-m nonCentralChi ' + \
                                 '-d 4 ' + \
                                 '-s 4'
			os.system( command )

			command = 'AimsFileConvert ' + \
                                 '-i '  + os.path.join( Dir,
					                '01-PrepareData',
					                '05-NonLocalMeansFiltering',
					                subject + '_' + session + '.nii ' ) + \
                                 '-o '  + os.path.join( Dir,
					                '01-PrepareData',
					                '05-NonLocalMeansFiltering',
					                subject + '_' + session + '.nii ' ) + \
                                 '-t S16 '
			os.system( command )

			command = 'rm -f ' + \
                                 os.path.join( Dir,
				                '01-PrepareData',
				                '05-NonLocalMeansFiltering',
				                '*.minf ' )
			os.system( command )
