function  DataSegmentation( BASEdir )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Wrote by David André Barrière 09th September 2022
% This function permit to create and launch Normalization and Segmentation
% processing using SPM8 function.
% Usage : set BASEdir variable with your current working directory 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Variables

    % SPM Batch to load
T = load( 'processing_step02_MultiSubject.mat' ) ; 

    % Filtered Data Directory
DataDir = [ BASEdir,...
            '/01-PrepareData',...
            '/05-NonLocalMeansFiltering/' ] ; 
        
    % Filtered Data List
NiiFiles = dir( fullfile(DataDir,...
                'sub*.nii' ) ) ; 
NiiFiles = { NiiFiles(:).name } ;

    % Prior image for Segmentation
Priors = { [ BASEdir, '/00-DataSet',...
                      '/Turone_Sheep_Brain_Template_And_Atlas',...
                      '/brain_Templates',...
                      '/prob01.nii' ],...
           [ BASEdir, '/00-DataSet',...
                      '/Turone_Sheep_Brain_Template_And_Atlas',...
                      '/brain_Templates',...
                      '/prob02.nii' ],...
           [ BASEdir, '/00-DataSet',...
                      '/Turone_Sheep_Brain_Template_And_Atlas',...
                      '/brain_Templates',...
                      '/prob03.nii' ] } ;
                  
    % Template image for Registration
Template = { [ BASEdir, '/00-DataSet',...
                        '/Turone_Sheep_Brain_Template_And_Atlas',...
                        '/brain_Templates',...
                        '/brain_ir_template.nii' ] } ; 
    % list of SPM function to run
TemplateJob = { [ BASEdir,...
                  '/processing_step02_Template.mat' ] } ;

    % Make output Directory
mkdir ( [ BASEdir,...
          '/02-LinearNormalisation' ]) ;
OutputDir = { [ BASEdir,...
                '/02-LinearNormalisation' ] } ;

    % Create SPM Batch
m = 1 ;
for i = 1 : 1 : length( NiiFiles )
    
    NII = { [ DataDir, '/', NiiFiles{i} ] } ;
    disp(NiiFiles{i}) ;
    
    T.matlabbatch{1}.cfg_basicio.runjobs.jobs = TemplateJob;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{1}.innifti = Template ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{2}.innifti = NII ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{3}.innifti = Priors ;
    T.matlabbatch{1}.cfg_basicio.runjobs.inputs{m}{4}.indir = OutputDir;
    m = m+1;
   
end

    % Run SPM Batch
matlabbatch = T.matlabbatch ;
save(  'processing_step02_MultiSubject_Loaded', 'matlabbatch'  ) ;
spm_jobman('run',matlabbatch);              
            