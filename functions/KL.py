import pandas as pd
import numpy as np

def KL_diagam(fin):

    ''' Koenig & Leisawitz (2014) colour-colour / colour magnitude diagrams with 2MASS and WISE filters

        fin [str]: Name of the csv file with the magnitudes 
    '''

    data= pd.read_csv(fin)

    test= data # auxiliar dataframe
    test['KL']= 'False'

    
    # Step 1: contaminants

    test_SFG = (
            (test['W2mag'] - test['W3mag'] > 2.3) & 
            (test['W1mag'] - test['W2mag'] < 1.0) & 
            (test['W1mag'] - test['W2mag'] < ((0.46 * (test['W2mag'] -test['W3mag'])) - 0.78)) &
            (test['W1mag'] > 13)
    )

    test= test[~test_SFG]

    test_AGN =(
    (test['W1mag'] > ((1.8 * (test['W1mag'] - test['W3mag'])) + 4.1)) & 
    (test['W1mag'] > 13)| 
    (test['W1mag'] > test['W1mag'] - test['W3mag'] + 11.0)
)


    test_YSO_AGN =(
       (test['W4mag'] < 5.0) &
        ((test['W2mag'] - test['W4mag'] > 4.5) & ((test['W2mag'] - test['W4mag']) < 8.0 )) &
        (test['W1mag'] - test['W2mag'] > 1.0 ) &
        (test['W3mag'] - test['W4mag'] > 2.0 )
    ) 
    
    AGN= test[test_AGN & ~test_YSO_AGN]
    test= test[~AGN]


    
    # Step 2: YSOs

    YSO_classI = (
        (test['W2mag'] - test['W3mag'] > 2.0 ) &
        (test['W2mag'] - test['W3mag'] < 4.5 ) &
        (test['W1mag'] - test['W2mag'] > 0.46 * (test['W2mag'] - test['W3mag']) - 0.9) &
        (test['W1mag'] - test['W2mag'] > -0.42 * (test['W2mag'] - test['W3mag']) + 2.2)
    )

    
    YSO_classII = (
        (test['W1mag'] - test['W2mag'] > 0.25) &
        (test['W1mag'] - test['W2mag'] < 0.9 * (test['W2mag'] - test['W3mag']) - 0.25) &
        (test['W1mag'] - test['W2mag'] > -1.5 * (test['W2mag'] - test['W3mag']) + 2.1) &
        (test['W1mag'] - test['W2mag'] > 0.46 * (test['W2mag'] - test['W3mag']) - 0.9) &
        (test['W2mag'] - test['W3mag'] < 4.5 )
    )
    
    
    YSO_2MASS = (
        (test['Hmag'] - test['Kmag'] > 0.0) &
        (test['Hmag'] - test['Kmag'] > -1.76 * (test['W1mag'] - test['W2mag']) + 0.9) &
        (test['Hmag'] - test['Kmag'] < (0.55 / 0.16) * (test['W1mag'] - test['W2mag']) - 0.85) &
        (test['W1mag'] <= 13.0)
    ) 
    
    YSO_trDisk = (
         (test['W3mag'] - test['W4mag'] > 1.5) &
         (((test['W1mag'] - test['W2mag']) > 0.15) & ((test['W1mag'] - test['W2mag']) < 0.80 )) & 
         (test['W1mag'] - test['W2mag'] > 0.46 * (test['W2mag'] - test['W3mag']) - 0.9 ) &
         (test['W1mag'] <= 13.0 )
    )
    
    
    YSO= YSO_classI | YSO_classII | YSO_2MASS | YSO_trDisk  
    test_yso= test[YSO]


    # Step 3: From YSOs drop AGBs

    test_AGB = (
        ((test_yso['W1mag'] < (-10.0/3.0) * (test_yso['W1mag'] - test_yso['W2mag']) + 9.0) |
        (test_yso['W1mag'] < (6.0/7.0) * (test_yso['W1mag'] - test_yso['W2mag']) + 5.5)) |
        ((test_yso['W3mag'] - test_yso['W4mag'] < 1.9) &
        (test_yso['W1mag'] - test_yso['W2mag'] < test_yso['W3mag'] - test_yso['W4mag'] - 0.45))
    )


    test.loc[YSO_trDisk, 'KL'] = 'trDisk'
    test.loc[YSO_2MASS, 'KL'] = 'Class II'
    test.loc[YSO_claseII, 'KL'] = 'Class II'
    test.loc[YSO_claseI, 'KL'] = 'Class I'
    
    test.loc[test_SFG, 'KL']= 'cont'
    test.loc[AGN, 'KL']= 'cont'
    test.loc[test_AGB, 'KL']= 'cont'

    data['KL']= test.KL
    data.to_csv(fin, index=False)
    
    