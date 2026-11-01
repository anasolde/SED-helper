import pandas as pd
import numpy as np
import os

import sedfitter_main.sedfitter as sd
import sedfitter_main.sedfitter.utils.io as io


def create_dir_safe(dir_name):
    os.makedirs(dir_name, exist_ok=True)




def plot_sed(folder_out, fileout_name, good_models, source_name):

    '''Sedfitter plot sed routine: https://sedfitter.readthedocs.io/en/stable/api/sedfitter.plot.html#sedfitter.plot

       folder_out (str): path of the directory with the outputs
       fileout_name (str): path of the output file 
       good_models (str): path of the csv file with number of good models (from reading routine)
       source_name (str): Prefix of the source

       '''

    io.create_dir = create_dir_safe     # avoid sedfitter rewrite folder
    
    result_file= pd.read_csv(fileout_name)
    result_good= pd.read_csv(good_models)
    result_good.set_index('Unnamed: 0', inplace=True)
   
    
    N= result_file.shape[0]
    fams_ok= list(result_file.Family)
    
    
    for source in range(N):
        families= []
        family= fams_ok[source]
        families.append(family)
    
        
        Ngood= res_good.loc[familia, source_name+str(source+1)]
        out_format= ('N', Ngood)  
    
        dst= folder_out+'fitinfo'
    
        file_output = dst+'/temp_file'+str(source)+'_'+family+'_out.fitinfo'
    
        sd.plot(file_output,
                output_dir=folder_out+'plots',
                format='pdf',
                plot_mode='A',
                select_format=('N', Ngood),                 #default= ('N',1)
                show_convolved=True, show_sed=True,      
                x_mode='A',
                y_mode='A',)
    
    


def plot_one_source(source, family, Ngood)

    ''' Plot a single fit 
    
        source (int): Number of the source (as in the fit)
        family (str): Family of the fit
        Ngood (int): Number of good models to plot along the best (if only the best is desired, Ngood=1)
        
        '''


    dst= folder_out+'fitinfo'
    
    file_output = dst+'/temp_file'+str(source-1)+'_'+family+'_out.fitinfo'
        
    sd.plot(file_output,
            output_dir=folder_out+'plots',
            format='pdf',
            plot_mode='A',
            select_format=('N', Ngood),                 #default= ('N',1)
            show_convolved=True, show_sed=True,      
            x_mode='A',
            y_mode='A',)
    

