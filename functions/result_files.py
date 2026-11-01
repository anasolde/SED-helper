import pandas as pd
import numpy as np

from astropy.table import Table
from astropy.io import fits


def best_fit (fin, folder_out, name_df, fileout_name, num_out, source_name):               

    '''Create csv file with source parameters by the model selection criterium chosen
       
       fin (str): name of the csv with data
       folder_out (str): path of the output directory

       name_df (str): to select among K9, F3, BIC or any other criterium created by user
       fileout_name (str): path of the new file
       num_out (int): Number of models of the output fit 
       source_name (str): Prefix of the source 
    '''

    data= pd.read_csv(fin)
    N_sample= data.shape[0]

    names= []
    for i in range(1,N_sample+1):
        names.append(source_name+str(i))


    Chi= pd.read_csv(folder_out+'df_Chi.csv')
    col= np.array(Chi.columns)               
    families= np.array(Chi['Unnamed: 0'])

    BIC= pd.read_csv(folder_out+'BIC.csv')
    BIC= BIC[col[1:]]
    BIC.index=families
     
    K9= pd.read_csv(folder_out+'K9.csv')    
    K9= K9[col[1:]]
    K9.index=families

    F3= pd.read_csv(folder_out+'F3.csv')
    F3= F3[col[1:]]
    F3.index=families
    
    models= pd.read_csv(folder_out+'Models.csv')
    models= models[col[1:]]
    models.index=families

    param_model= pd.DataFrame(index=col[1:])
    param_model['Source']= names
    param_model['RAJ2000']= data.RAJ2000
    param_model['DEJ2000']= data.DEJ2000
    

    

    dataframes= {
        'K9': [False, K9],
        'F3': [False, F3],
        'BIC': [True, BIC],
        'Chi': [True, Chi]
    }

    order= dataframes[name_df][0]
    df= dataframes[name_df][1]


    fams_avail=[]
    for j in col[1:]:
        notnas= df[str(j)].notna()
        fams_avail.append(df[str(j)][notnas].sort_values(ascending=order).index.values)
        
      
    
    best_model=[]           # Model for each source
    family_model=[]         # Family of the best model
    best_stage=[]            # Stage of the best model
    best_class=[]            # Class of the best model



    
    Teff, Av, Scale, Alpha = [],[],[],[]
    best_Chi = []
    
    for i in range(N_sample) :        
        source = fams_avail[i]
        best_fam= source[0]
                                                     
    
        best_model.append(models[source_name+str(i+1)][str(best_fam)])
        family_model.append(best_fam)
    
        hdu_info= fits.open(best_fam+'/info.fits')
        t2= Table(hdu_info[1].data)
        selection2 = np.isin(t2['Model Name'], best_model)
        subtable2 = t2[selection2]
    
        best_stage.append(list(subtable2['Stage'])[0])
        best_class.append(list(subtable2['Class'])[0])
    
    
        # Parameters of sedfitter output
    
        file= folder_out+'result_'+best_fam+'/parameters_'+best_fam+'.csv'
        param_physics= pd.read_csv(file, engine='python')

        Teff.append(param_physics['Teff'][i])
        Av.append(param_physics['Av'][i])
        Scale.append(param_physics['Scale'][i])
        Alpha.append(param_physics['Alpha'][i])

            
        file_chi = folder_out+'result_'+best_fam+'/best'+best_fam+'.txt'
        
        with open(file_chi, "r", encoding="utf-8") as ms:
            lines = ms.readlines()
        
            indice = 2+ (num_out+1)*(i) +2
            
            line = lines[indice]
            elements = line.split()
            best_Chi.append(elements[2])     
              
    
    param_model['Family']= family_model
    param_model['Model']= best_model
    # param_model['Stage']= best_stage       Richardson, T. (2024) stage
    # param_model['Class']= best_class       Richardson, T. (2024) class
    param_model['Chi']= best_Chi

    

    # Geometry by families

    param_model.loc[param_model['Family'] == 's---s-i', 'Geometry'] = 'Bare'
    param_model.loc[param_model['Family'] == 'sp--s-i', 'Geometry'] = 'Disk'
    param_model.loc[param_model['Family'] == 'sp--h-i', 'Geometry'] = 'Disk'
    param_model.loc[param_model['Family'] == 's---smi', 'Geometry'] = 'Bare'
    param_model.loc[param_model['Family'] == 'sp--smi', 'Geometry'] = 'Disk'
    param_model.loc[param_model['Family'] == 'sp--hmi', 'Geometry'] = 'Disk'
    param_model.loc[param_model['Family'] == 's-p-smi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-p-hmi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-pbsmi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-pbhmi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-u-smi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-u-hmi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-ubsmi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 's-ubhmi', 'Geometry'] = 'Envelope'
    param_model.loc[param_model['Family'] == 'spu-smi', 'Geometry'] = 'Env + disk'
    param_model.loc[param_model['Family'] == 'spu-hmi', 'Geometry'] = 'Env + disk'
    param_model.loc[param_model['Family'] == 'spubsmi', 'Geometry'] = 'Env + disk'
    param_model.loc[param_model['Family'] == 'spubhmi', 'Geometry'] = 'Env + disk'
        

    
    param_model['Teff']= Teff
    param_model['Av']= Av
    param_model['Scale']= Scale        # related to distance
    param_model['Alpha']= Alpha        # spectral index


    

    param_model['Teff_gaia']= data.Teff
    param_model['b_Teff_gaia']= data.b_Teff
    param_model['B_Teff_gaia']= data.B_Teff
    param_model['A0_gaia']= data.A0
    param_model['b_A0_gaia']= data.b_A0
    param_model['B_A0_gaia']= data.B_A0
    param_model['rgeo_BJ']= data.rgeo
    param_model['b_rgeo_BJ']= data.b_rgeo
    param_model['B_rgeo_BJ']= data.B_rgeo
    param_model['KL']= data.KL

    

    param_model['SPT_fit']= get_sptype(Teff)
    param_model['Class_fit']= get_sptype(Alpha)

    param_model.to_csv(fileout_name, index=False)



    
    
def get_sptype(teff):
    '''Classify in MK spectral types by temperature'''

    skiff_ranges = {
        'O': (20000, 100000),
        'B': (10000, 20000),
        'A': (7500, 10000),
        'F': (6000, 7500),
        'G': (5200, 6000),
        'K': (3700, 5200),
        'M': (0, 3700)
    }
    
    for sp, (tmin, tmax) in skiff_ranges.items():
        if tmin <= teff < tmax:
            return sp
    return None



def get_class(alpha):
    '''Classify in evolutionary classes by spectral index'''

    class_ranges = {
        'Class I': (0.3, 100000),
        'Flat': (-0.3, 0.3),
        'Class II': (-1.6, -0.3),
        'Class III': (-2.5, -1.6),
        'b/MS': (-10000, -2.5)
    }
    
    for cl, (cl_min, cl_max) in class_ranges.items():
        if cl_min <= alpha < cl_max:
            return cl
    return None
















    

    





def 





