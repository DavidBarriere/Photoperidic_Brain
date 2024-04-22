#-----------------------------------------------------------------------------
# Wrote by David André Barrière 09th September 2022
#
# This function is derived from the "Second-level fMRI model: 
# two-sample test, unpaired and paired" example provided by the nilearn 
# package documentation.
#
# (https://nilearn.github.io/dev/auto_examples/05_glm_second_level/plot_second_level_two_sample_test.html)
#
# Analysis is done via a paired two-sample Student's T-test 
# with a p-value of 0.005 (T score = 2.920782).
#
#-----------------------------------------------------------------------------

import sys, os, string, inspect, types, glob, fnmatch, re, copy, shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from nilearn import plotting
from nilearn.plotting import plot_design_matrix
from nilearn.glm.second_level import SecondLevelModel
from nilearn.datasets import fetch_localizer_contrasts

from CopyFileDirectoryRm import *

def runDataVisualization( Dir,
                          verbose ):
                          
	if ( verbose == True ):
           
				#-------------------------------------------------------------------------
				# Make Directories
				#-------------------------------------------------------------------------
		outputDir = os.path.join( Dir,
															'05-Results' )

		AxialDir = os.path.join( Dir,
														 '05-Results',
														 'Axial' )

		SaggitalDir = os.path.join( Dir,
																'05-Results',
																'Saggital' )

		CoronalDir = os.path.join( Dir,
															 '05-Results',
															 'Coronal' )

		AxialDir_thr1 = os.path.join( Dir,
														 			'05-Results',
														 			'Axial',
															 		'thr1' )


		SaggitalDir_thr1 = os.path.join( Dir,
																		 '05-Results',
																		 'Saggital',
															 			 'thr1' )


		CoronalDir_thr1 = os.path.join( Dir,
															 			'05-Results',
															 			'Coronal',
															 			'thr1' )

		AxialDir_thr2 = os.path.join( Dir,
														 			'05-Results',
														 			'Axial',
															 		'thr2' )

		SaggitalDir_thr2 = os.path.join( Dir,
																		 '05-Results',
																		 'Saggital',
															 			 'thr2' )

		CoronalDir_thr2 = os.path.join( Dir,
															 			'05-Results',
															 			'Coronal',
															 			'thr2' )

		AxialDir_thr3 = os.path.join( Dir,
														 			'05-Results',
														 			'Axial',
														 			'thr3' )

		SaggitalDir_thr3 = os.path.join( Dir,
																		 '05-Results',
																		 'Saggital',
																		 'thr3' )

		CoronalDir_thr3 = os.path.join( Dir,
															 			'05-Results',
															 			'Coronal',
															 			'thr3' )

		turone_template_filename = os.path.join( Dir,
																						 '00-DataSet',
																						 'Turone_Sheep_Brain_Template_And_Atlas',
																						 'brain_Templates',
																						 'brain_t1_template.nii' )

		turone_mask_filename = os.path.join( Dir,
																				 '00-DataSet',
																				 'Turone_Sheep_Brain_Template_And_Atlas',
																				 'brain_Templates',
																				 'GM_mask.nii' )

		makedir( outputDir )
		makedir( AxialDir )
		makedir( SaggitalDir )
		makedir( CoronalDir )
		makedir( AxialDir_thr1 )
		makedir( SaggitalDir_thr1 )
		makedir( CoronalDir_thr1 )
		makedir( AxialDir_thr2 )
		makedir( SaggitalDir_thr2 )
		makedir( CoronalDir_thr2 )
		makedir( AxialDir_thr3 )
		makedir( SaggitalDir_thr3 )
		makedir( CoronalDir_thr3 )

		print( 'Directories created in ' + Dir )
		print( ' ' )

				#-------------------------------------------------------------------------
				# Define the input maps
				#-------------------------------------------------------------------------
		sample_winter = glob.glob(os.path.join( Dir,
																						'04-StatisticalAnalysis',
																						'Data',
																						'swwc1rsub-*_ses-1.nii' ))
		sample_summer = glob.glob(os.path.join( Dir,
																						'04-StatisticalAnalysis',
																						'Data',
																						'swwc1rsub-*_ses-2.nii' ))
		sample_winter.sort()
		sample_summer.sort()

				#-------------------------------------------------------------------------
				# Modelization of the effect (sample 1 vs sample 2)
				#-------------------------------------------------------------------------
		n_subjects = 17

		second_level_input = sample_winter + sample_summer

		condition_effect = np.hstack(( [-1] * n_subjects,
																	 [1] * n_subjects ))

		subject_effect = np.vstack(( np.eye( n_subjects ),
																 np.eye( n_subjects )))

		subjects = [f'S{i:02d}' for i in range( 1,
																						n_subjects + 1 )]

		unpaired_design_matrix = pd.DataFrame( condition_effect[ :,
					                                            			 np.newaxis ],
					                           			 columns=[ 'winter vs summer' ])

		paired_design_matrix = pd.DataFrame(np.hstack(( condition_effect[ :,
																																			np.newaxis ],
																										subject_effect )),
																										columns=[ 'winter vs summer' ] + subjects )

		_, ( ax_unpaired, ax_paired ) = plt.subplots( 1,
																									2,
																									gridspec_kw={'width_ratios': [ 1,
																																								 17 ]})
		plot_design_matrix( unpaired_design_matrix,
												rescale=False,
												ax=ax_unpaired)

		plot_design_matrix( paired_design_matrix,
												rescale=False,
												ax=ax_paired )

		ax_unpaired.set_title( 'unpaired design',
													 fontsize=12 )

		ax_paired.set_title( 'paired design',
												 fontsize=12 )

		plt.tight_layout()

		plt.savefig( os.path.join( Dir,
					                     '05-Results',
					                     'contrast.png' ),
					                     dpi=900 )
		
		print( 'Modelization of the effect (Winter vs Summer)' )
		print( 'Number of animals = ' +  str( n_subjects ) )
		print( 'Number of conditions = 2' )
		print( ' ' )

				#-------------------------------------------------------------------------
				# Model fitting
				#-------------------------------------------------------------------------
		print( 'Second Level Model unPaired Fitting' )
		print( 'Mask used = ' +  turone_mask_filename )
		print( 'smoothing (fwhm) = 1' )
		print( ' ' )
		
		second_level_model_unpaired = SecondLevelModel( mask_img = turone_mask_filename,
					                                    			smoothing_fwhm=1 ).fit( second_level_input,
					                                                            			design_matrix=unpaired_design_matrix )

		print( 'Second Level Model Paired Fitting' )
		print( 'Mask used = ' +  turone_mask_filename )
		print( 'smoothing (fwhm) = 1' )
		print( ' ' )
		second_level_model_paired = SecondLevelModel( mask_img = turone_mask_filename,
																									smoothing_fwhm=1 ).fit( second_level_input,
					                                                          			design_matrix=paired_design_matrix )

		stat_maps_unpaired = second_level_model_unpaired.compute_contrast( 'winter vs summer',
					                                                       			 output_type='all')

		stat_maps_paired = second_level_model_paired.compute_contrast( 'winter vs summer',
					                                                       	 output_type='all')

				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Saggital View threshold 0.05
				#-------------------------------------------------------------------------
		print( 'Writting Saggital Data in ' + SaggitalDir_thr1 )
		print( 'Threshold (T-map) = 1.75' )
		print( 'p-value = 0.05' )
		print( 'dof = 16' )
		print( ' ' )
		
		i = 0
		
		for n in range (0,30,1):
				i=i+1
				outputSlice = os.path.join( SaggitalDir_thr1,
					                    			'slice_00' + str(i) + '_Saggital.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=1.75,
					                			cut_coords=( n, 58, 66 ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=300 )
					     
				print( outputSlice )
				
		print( ' ' )

				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Coronal View threshold 0.05
				#-------------------------------------------------------------------------
		print( 'Writting Coronal Data in ' + CoronalDir_thr1 )
		print( 'Threshold (T-map) = 1.75' )
		print( 'p-value = 0.05' )
		print( 'dof = 16' )
		print( ' ' )
		
		i = 0
		
		for n in range (-50,50,1):
				i=i+1
				outputSlice = os.path.join( CoronalDir_thr1,
					                    			'slice_00' + str(i) + '_Coronal.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=1.75,
					                			cut_coords=( 36, 58, n ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=300 )
					     
				print( outputSlice )
				
		print( ' ' )
		"""
				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Axial View  threshold 0.05
				#-------------------------------------------------------------------------
		print( 'Writting Axial Data in ' + AxialDir_thr1 )
		print( 'Threshold (T-map) = 1.75' )
		print( 'p-value = 0.05' )
		print( 'dof = 16' )
		print( ' ' )

		i = 0
		
		for n in range (-40,55,1):
				i=i+1
				outputSlice = os.path.join( AxialDir_thr1,
					                    			'slice_00' + str(i) + '_Axial.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=1.75,
					                			cut_coords=( 36, n, 66 ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=900 )

				print( outputSlice )
		"""
				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Saggital View threshold 0.01
				#-------------------------------------------------------------------------
		print( 'Writting Saggital Data in ' + SaggitalDir_thr2 )
		print( 'Threshold (T-map) = 2.58' )
		print( 'p-value = 0.01' )
		print( 'dof = 16' )
		print( ' ' )
		
		i = 0
		
		for n in range (0,30,1):
				i=i+1
				outputSlice = os.path.join( SaggitalDir_thr2,
					                    			'slice_00' + str(i) + '_Saggital.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=2.58,
					                			cut_coords=( n, 58, 66 ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=300 )
					     
				print( outputSlice )
				
		print( ' ' )

				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Coronal View threshold 0.01
				#-------------------------------------------------------------------------
		print( 'Writting Coronal Data in ' + CoronalDir_thr2 )
		print( 'Threshold (T-map) = 2.58' )
		print( 'p-value = 0.01' )
		print( 'dof = 16' )
		print( ' ' )
		
		i = 0
		
		for n in range (-50,50,1):
				i=i+1
				outputSlice = os.path.join( CoronalDir_thr2,
					                    			'slice_00' + str(i) + '_Coronal.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=2.58,
					                			cut_coords=( 36, 58, n ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=300 )
					     
				print( outputSlice )
				
		print( ' ' )
		"""
				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Axial View threshold 0.01
				#-------------------------------------------------------------------------
		print( 'Writting Axial Data in ' + AxialDir_thr2 )
		print( 'Threshold (T-map) = 2.58' )
		print( 'p-value = 0.01' )
		print( 'dof = 16' )
		print( ' ' )

		i = 0
		
		for n in range (-40,55,1):
				i=i+1
				outputSlice = os.path.join( AxialDir_thr2,
					                    			'slice_00' + str(i) + '_Axial.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=2.58,
					                			cut_coords=( 36, n, 66 ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=900 )

				print( outputSlice )
		"""
				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Saggital View threshold 0.005
				#-------------------------------------------------------------------------
		print( 'Writting Saggital Data in ' + SaggitalDir_thr3 )
		print( 'Threshold (T-map) = 2.92' )
		print( 'p-value = 0.005' )
		print( 'dof = 16' )
		print( ' ' )
		
		i = 0
		
		for n in range (0,30,1):
				i=i+1
				outputSlice = os.path.join( SaggitalDir_thr3,
					                    			'slice_00' + str(i) + '_Saggital.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=2.92,
					                			cut_coords=( n, 58, 66 ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=300 )
					     
				print( outputSlice )
				
		print( ' ' )

				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Coronal View threshold 0.005
				#-------------------------------------------------------------------------
		print( 'Writting Coronal Data in ' + CoronalDir_thr3 )
		print( 'Threshold (T-map) = 2.92' )
		print( 'p-value = 0.005' )
		print( 'dof = 16' )
		print( ' ' )
		
		i = 0
		
		for n in range (-50,50,1):
				i=i+1
				outputSlice = os.path.join( CoronalDir_thr3,
					                    			'slice_00' + str(i) + '_Coronal.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=2.92,
					                			cut_coords=( 36, 58, n ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=300 )
					     
				print( outputSlice )
				
		print( ' ' )
		"""
				#-------------------------------------------------------------------------
				# Write paired student's T-test results - Axial View threshold 0.005
				#-------------------------------------------------------------------------
		print( 'Writting Axial Data in ' + AxialDir_thr3 )
		print( 'Threshold (T-map) = 2.92' )
		print( 'p-value = 0.005' )
		print( 'dof = 16' )
		print( ' ' )

		i = 0
		
		for n in range (-40,55,1):
				i=i+1
				outputSlice = os.path.join( AxialDir_thr3,
					                    			'slice_00' + str(i) + '_Axial.png' )

				plotting.plot_stat_map( stat_maps_paired['z_score'],
					                			bg_img=turone_template_filename,
					                			draw_cross=False,
					                			threshold=2.92,
					                			cut_coords=( 36, n, 66 ),
					                			dim=-0.5,
					                			alpha=0.7,
					                			vmax=7,
					                			resampling_interpolation='continuous')

				plt.savefig( outputSlice,
										 dpi=900 )

				print( outputSlice )
		"""
