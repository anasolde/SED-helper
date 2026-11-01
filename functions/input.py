import pandas as pd
import numpy as np
import sys

def input_sedfitter(fin, fout, RA, DE, bands, zero_points, confidence):     #fin

    """Given input file, keys of RA and DEC in dataframe, bands to use in the fit, zeropoints of these bands and confidence of measurements without 
       error, the function creates output txt file to use as input in Sedfitter algorithm

       fin (str): name of the csv with data
       fout (str): name of the input file in the algorithm
       RA, DE (str): keys of RA, DEC coordinates in csv
       bands (list[str]): name of filters in mag
       zero_points (array): zero points of the bands in mJy in same order as bands
                https://svo2.cab.inta-csic.es/theory/fps3/
       confidence (float): confidence in measures without available error [0,1]
       
      """

    df = pd.read_csv(fin)
    
    souces_names= []
    for i in range(1,df.shape[0]+1):
        souces_names.append('src'+str(i))
    
    df['Name']= souces_names
    
    coord= []
    coord.append(RA)
    coord.append(DE)
    
    zeros= {}

    if len(bands) == len(zero_points):

        for i in range(len(bands)):
            zeros[bands[i]]= zero_points[i]

    else:
        sys.exit('Number of bands does not correspond to number of zeropoints')
        
        
    
    flags, fluxes = [],[]
    
    for b in bands:
        mag = f'{b}mag'
        emag = f'e_{b}mag'
        flag = f'flag{b}'

               
        df[flag]= len(df)*['0']
        df[flag] = np.where(df[mag].isna(),0,np.where(df[emag].isna(),3,1))

        zero= zeros[b]
        flux= zero*10**(-0.4*df[mag])
        error= flux*df[emag]*np.log(10)/2.5
        
        df[b]= flux
        df['e_'+b]= error
    
        flags.append(flag)
        fluxes.extend([b, 'e_'+b])
    
    df_flux= df[['Name'] + coord + flags + fluxes]
    
    
    
    for b in bands:
        f = f'{b}'
        ef = f'e_{b}'
        flag = f'flag{b}'

        
    
        if ef in df_flux.columns and flag in df_flux.columns:
            mask = (df_flux[flag] == 3) & (df_flux[ef].isna())
            df_flux.loc[mask, ef] = confidence                           
            
    
    df_flux = df_flux.fillna(0.0)   # Substitute NaN values with 0.0
    df_flux.to_csv(fout, sep=' ', index=False, header=False)


