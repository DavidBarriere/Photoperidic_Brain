function  DataFixHeader( BASEdir )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Wrote by David André Barrière 09th September 2022
% This function permit to fix header of corrected data for SPM running.
% Usage : set BASEdir variable with your current working directory 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Variables
    % Template image for Registration
Template = [ BASEdir,...
             '/00-DataSet',...
             '/Turone_Sheep_Brain_Template_And_Atlas',...
             '/brain_Templates',...
             '/brain_ir_template.nii' ] ;

Ref_Header = spm_vol_nifti( Template ) ;
Ref_Matrix = spm_read_vols( Ref_Header ) ;

    % Filtered Data Directory
DataDir = [ BASEdir,...
            '/01-PrepareData',...
            '/05-NonLocalMeansFiltering/' ] ; 
        
    % Filtered Data List
NiiFiles = dir( fullfile(DataDir,...
                'sub*.nii' ) ) ; 
NiiFiles = { NiiFiles(:).name } ;

for i = 1 : 1 : length( NiiFiles )
    Nifti_Header = spm_vol_nifti( [ DataDir,...
                                    NiiFiles{i} ] ) ;
    Nifti_Matrix = spm_read_vols( Nifti_Header ) ;
    Nifti_Matrix = flip( Nifti_Matrix,3 ) ;
    Nifti_Matrix = flip( Nifti_Matrix,2 ) ;
    Ref_Header.fname = Nifti_Header.fname ;
    spm_write_vol( Ref_Header,...
                   Nifti_Matrix ) ;

end

