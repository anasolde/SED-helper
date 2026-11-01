import pandas as pd
import numpy as np
import sys
import scipy.stats as sc
import matplotlib.pyplot as plt
import os
import shutil
import tempfile
from pathlib import Path

from astropy import units as u
from astropy.table import Table
from astropy.io import fits

import sedfitter_main.sedfitter as sd
from sedfitter_main.sedfitter.sed import SEDCube
from sedfitter_main.sedfitter.extinction import Extinction


def read_results(fin, folder_out, K_thres, F_thres, families, source_name):

    '''Read the output files with parameters and create K, F, BIC files with selected threshold
       
       fin (str): name of the csv with data
       folder_out (str): path of the output directory

       K_thres (int): threshold (multiplied by ndata) to use in K method
       F_thres (int): threshold (multiplied by ndata) to use in F method

       families (list[str]): families used in the fit
       source_name (str): Prefix of the source 
    '''

    
    data= pd.read_csv(fin)
    N_sample= data.shape[0]

    
    names= []
    for i in range(1,N_sample+1):
        names.append(source_name+str(i))


    #-----------------------------------------------------------------------------------------------------
    # Number of templates in each family (in this case, after filtering by above MS)
    num_eachmodel= [7552,67995,67545,7646,67866,67318,6762,6864,56554,59427,64594,65475,64490,64685,64475,65229,254704,513316]

    # if every template is used in the fit
    # num_eachmodel= [10000,90000,90000, 10000,90000,90000,10000,10000,90000, 90000, 90000, 90000, 90000, 90000, 90000, 90000,360000,720000]

    #----------------------------------------------------------------------------------------------------
    
    
    Nmodels= pd.DataFrame(np.tile(np.array(num_eachmodel).reshape(-1, 1), (1, N_sample)), index=families, columns= names)
    
    
    Nfit= []
    Ndat= []
    Chi2= []
    Models= []
    
    
    for fam in families:
        model_file= folder_out+'result_'+str(fam)+'/best'+str(fam)+'.txt'
        
        with open(model_file,'r') as models:
        
            for _ in range(3):             # Header
                next(models)
            
            table_model= []
            table_chi= []
            table_data= []
            table_fit=[]

            for j in range(N_sample):         # Fits every sources for a family
                cab= next(models).split()
                
                ndata= int(cab[1])
                nfits= int(cab[2])
                
                model_fit=[]
                chi_fit=[]
                
                for i in range(nfits):               # For each source
                    fit = next(models).split()
                    model_fit.append((fit[1]))
                    chi_fit.append(float(fit[2]))
                    
                table_model.append(model_fit[0])
                table_chi.append(chi_fit)
                table_data.append(ndata)
                table_fit.append(nfits)
    
            Chi2.append(table_chi)
            Models.append(table_model)
            Ndat.append(table_data)                   # Ndat and Nfit are unique for family and source
            Nfit.append(table_fit)
        
              
    
    all_nfit= pd.DataFrame(Nfit, columns=names, index=families)
    all_ndat= pd.DataFrame(Ndat, columns=names, index=families)
    all_chi= pd.DataFrame(Chi2, columns=names, index=families)
    all_models= pd.DataFrame(Models, columns=names, index=families)
    
    
    
    best_Chi= []
    
    for i in range(len(Chi2)):
        chi_source= []
        
        for j in range(len(Chi2[0])):
            chi=Chi2[i][j]
            chi_source.append(min(chi))
        best_Chi.append(chi_source)
    
    df_Chi= pd.DataFrame(best_Chi, columns=names, index=families)
    
    df_Chi.to_csv(folder_out+'df_Chi.csv', index=True)
    all_ndat.to_csv(folder_out+'Npoint.csv', index=True)
    all_models.to_csv(folder_out+'Models.csv', index=True)
    
    #########################################################################################

    # Method F
    # Fit chi2-chi2best < t·ndata 
    # choose chi2best for each family 
    
    Good_F3= pd.DataFrame(columns= all_chi.columns, index= all_chi.index)
    
    for i in names:
        column_f3=[]
        for j in families:
            column_f3.append(sum((all_chi[i][j] - df_Chi[i][j]) < F_thres*10))   # ndata= 10  
    
        Good_F3[i]= column_f3
            
    Good_F3.to_csv(folder_out+'Nfits_F3.csv', index= True)

    F3= pd.DataFrame(columns= all_chi.columns, index= all_chi.index)
    F3= Good_F3 / Nmodels
    F3.to_csv(folder_out+'F3.csv', index= True)


    #########################################################################################
    
    # Method K
    # Fit chi2-chi2total < t·ndata 
    # choose chi2total for each source (for each column)
    
    good=[]
    
    # First loop to get Chi2total
    
    for j in range(len(Chi2[0])):     
        best=[]                            # min of each cell
        for i in range(len(Chi2)):      
            list_chi= Chi2[i][j]
            best.append(list_chi[0])
        total= min(best)
    
    # Second loop to get Nfits
    
        fit=[]
        for i in range(len(Chi2)):
            list_chi= Chi2[i][j]
            criteria=[]
            for k in list_chi:
                criteria.append(k-total < K_thres*10)         # different criteria
            fit.append(sum(criteria))
        good.append(fit)
    
    Good_models= pd.DataFrame(good, index=names, columns=families).transpose()
    Good_models.to_csv(folder_out+'Good_K9.csv', index=True)
    
    Nfits_rel= Good_models / Nmodels
    Nfits_K9= pd.DataFrame()
    
    for i in names:
        Nfits_K9[str(i)]= Nfits_rel[str(i)] / np.mean(Nfits_rel[str(i)])
    
    Nfits_K9.to_csv(folder_out+'K9.csv', index=True)



     ########################################################################################
    
    # Bayesian criterium 
    
    # AIC= -2*np.log(likelihood) + 2*n_par
    # BIC= -2*np.log(likelihood) + n_par*np.log(Ndata)
    
    
    # n_par=[]
    for fam in families:
        model_file= folder_out+'result_'+str(fam)+'/best'+str(fam)+'.txt'
        with open(model_file,'r') as file:
            lines = file.readlines()
            # n_par.append(len(lines[4].split())-5)    

    n_par= [4,10,11,4,10,11,6,7,10,11,7,8,10,11,11,12,14,15]
    
    BIC= []
    
    for i in range(len(Chi2)):
        bic_source= []
    
        for j in range(len(Chi2[0])):
            bic= best_Chi[i][j] + n_par[i]*np.log(Ndat[i][j])         # -2*np.log(likelihood) = Chi         
            bic_source.append(bic)
        BIC.append(bic_source)
    
    df_BIC= pd.DataFrame(BIC, columns=names, index=families)
     
    df_BIC.to_csv(folder_out+'BIC.csv', index=True)

#------------------------------------------------------------------------------------------------------



    # Create parameters file in folder_out
       
    
    names= []
    for i in range(1,data.shape[0]+1):
        names.append('src'+str(i))



    for fam in families:
        model_file= folder_out+'result_'+str(fam)+'/best'+str(fam)+'.txt'
    
        Av=[]
        Scale=[]
        Teff=[]
        Alpha=[]
        
        with open(model_file,'r') as models:
                
            for _ in range(3):             # Header
                next(models)
            
            for j in range(N_sample):             
                cab= next(models).split()
                
                ndata= int(cab[1])
                nfits= int(cab[2])  
                
                fit = next(models).split()
                Av.append(float(fit[3]))
                Scale.append(float(fit[4]))
                Teff.append(float(fit[6]))      
                Alpha.append(float(fit[-1]))
                
        
                for _ in range(nfits-1):
                    next(models)
    
        
        par_file= pd.DataFrame(index= names)
        par_file['Av']= Av
        par_file['Scale']= Scale
        par_file['Teff']= Teff
        par_file['Alpha']= Alpha
        par_file.to_csv(folder_out+'result_'+str(fam)+'/parameters_'+str(fam)+'.csv')


