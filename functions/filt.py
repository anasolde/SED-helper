import numpy as np
import pandas as pd
import os
import shutil
from astropy.io import fits


def filter_aboveMS(listInstruments, directories, tempe_lim, outDir):

    '''Filter and select only the templates above MS and with valid values of Teff (above user limit)

       listInstruments (list[str]): Instruments used
       directories (list[str]): Directories with grid templates
       tempe_lim (float): Lower limit temperature
       outDir (str): Name of the directory where save new filter templates

       '''

    fichInfo='info.fits'
    fichStellar='stellar.fits'
    fichParameters='parameters.fits'
    fichFlux='flux.fits'
    fichCopiar= 'models.conf'
    
    
    #if needed, create a directory to save the files with only sources above the MS 
    if not os.path.exists(outDir):
        os.makedirs(outDir, exist_ok=True)
    
    for directory in directorys:
        if not os.path.isdir(directory):
            continue
        pathInfo=os.path.join(directory, fichInfo)
        with fits.open(pathInfo) as hdul:
            metaMS = hdul[0].header
            infoMS = hdul[1].data
            headerMS = hdul[1].header
        
        # Step 1: Above MS != 0
        MSStars=infoMS[infoMS['Above MS']!=0]
        print("File info.fits:", infoMS)
        print("--------------------------------------------------"  )
        print(fichInfo)
        print(pathInfo)
    
    
        # Step 2: Teff model > 2000
        pathParams=os.path.join(directory, fichParameters)
        with fits.open(pathParams) as hdu_par:
            headerPars=hdu_par[0].header
            model_namesPar = hdu_par[1].data
            headerModelsPar=hdu_par[1].header
    
        cTempe=(model_namesPar['star.temperature']>=tempe_lim)
        modsTempe=model_namesPar['MODEL_NAME'][cTempe]
    
    
        filtered_models=[nmod for nmod in MSStars['Model Name'] if (nmod in modsTempe)]
        nModSelel=len(filtered_models)
    
        print("Stars above MS and with Teff > 2000: "+str(tempe_lim)+': ', nModSelel)
        
    
        #write the MSStars to a fits file
        outDirMod=os.path.join(outDir, directory)
        os.makedirs(outDirMod, exist_ok=True)
        pathMSOut=os.path.join(outDirMod, fichInfo)
            # Primary HDU (for metadata)
        hduMS = fits.PrimaryHDU()
        hduMS.header = metaMS
        hduMS.header['NMODELS'] = nModSelel
    
        # Convolved fluxes
        idx = np.isin(MSStars['Model Name'], filtered_models)
        msSelected=MSStars[idx]
        hdu1 = fits.BinTableHDU(msSelected, name='INFO')
        hdu1.data = msSelected
        hdu1.header = headerMS
        hdu1.header['NMODELS'] = nModSelel
    
        hdulist = fits.HDUList([hduMS, hdu1])
        hdulist.writeto(pathMSOut)
        print(f"Convolved file saved: {pathMSOut}")
    
        # Save parameters file
        idx = np.isin(model_namesPar['MODEL_NAME'], filtered_models)
        modSelected=model_namesPar[idx]
        hdu0 = fits.PrimaryHDU(header=headerPars)
        hdu1 = fits.BinTableHDU(modSelected, name='MODEL_NAME', header=headerModelsPar)
        
        hdu0.header['NMODELS'] = nModSelel
        hdu1.header['NAXIS2'] = nModSelel
        
        pathParOut = os.path.join(outDirMod, fichParameters)
        fits.HDUList([hdu0, hdu1]).writeto(pathParOut, overwrite=True)
        print(f" Parameters file saved: {pathParOut}")
    
    
        # Stellar
        pathStellar=os.path.join(directory, fichStellar)
        with fits.open(pathStellar) as hdu_st:
            prim = hdu_st[0].data
            headPrim= hdu_st[0].header
            model_names = hdu_st[1].data
            headModels= hdu_st[1].header
            specINFO = hdu_st[2].data
            headSpec= hdu_st[2].header
            vals = hdu_st[3].data
            headVals= hdu_st[3].header
        idx=np.isin(model_names['MODEL_NAME'], filtered_models)
        primAboveMS=prim[idx]
        modelsAboveMS=model_names[idx]
        valsAboveMS=vals[idx]
        hdu0 = fits.PrimaryHDU(primAboveMS,header=headPrim)
        hdu1 = fits.BinTableHDU(modelsAboveMS, name='MODEL_NAMES', header=headModels)
        hdu2 = fits.BinTableHDU(specINFO, name='SPECTRAL_INFO', header=headSpec)
        hdu3 = fits.ImageHDU(valsAboveMS, name='VALUES', header=headVals)
        nModSel=len(filtered_models)
        hdu0.header['NAXIS1'] = nModSelel
        hdu0.header['NMODELS'] = nModSelel
        hdu1.header['NAXIS2'] = nModSelel
        hdu3.header['NAXIS3'] = nModSelel
    
        pathStOut=os.path.join(outDirMod, fichStellar)
        fits.HDUList([hdu0, hdu1, hdu2, hdu3]).writeto(pathStOut, overwrite=True)
        print(f" Stellar file saved: {pathStOut}")
    
        # Flux
        pathFlux=os.path.join(directory, fichFlux)
        with fits.open(pathFlux) as hdu_fx:
            prim= hdu_fx[0].data
            headPrim= hdu_fx[0].header
            model_names = hdu_fx[1].data
            headModels= hdu_fx[1].header
            specINFO = hdu_fx[2].data
            headSpec= hdu_fx[2].header
            apertures = hdu_fx[3].data
            headApert= hdu_fx[3].header
            vals1 = hdu_fx[4].data
            headVals= hdu_fx[4].header
            uncert = hdu_fx[5].data
            headUncert= hdu_fx[5].header
    
        idx = np.isin(model_names['MODEL_NAME'], filtered_models)
        primSelected=prim[idx]
        modSelected=model_names[idx]
        valsSelected=vals1[idx]
        uncertSelected=uncert[idx]
        hdu0 = fits.PrimaryHDU(primSelected,header=headPrim)
        hdu1 = fits.BinTableHDU(modSelected, name='MODEL_NAMES', header=headModels)
        hdu2 = fits.BinTableHDU(specINFO, name='SPECTRAL_INFO', header=headSpec)
        hdu3 = fits.BinTableHDU(apertures, name='APERTURES', header=headApert)
        hdu4 = fits.ImageHDU(valsSelected, name='VALUES', header=headVals)
        hdu5 = fits.ImageHDU(uncertSelected, name='UNCERTAINTIES', header=headUncert)
        
        hdu0.header['NMODELS'] = nModSelel
        hdu0.header['NAXIS1'] = nModSelel
        hdu1.header['NAXIS2'] = nModSelel
        hdu4.header['NAXIS3'] = nModSelel
        hdu5.header['NAXIS3'] = nModSelel
    
        pathFluxOut = os.path.join(outDirMod, fichFlux)
        fits.HDUList([hdu0, hdu1, hdu2, hdu3, hdu4, hdu5]).writeto(pathFluxOut, overwrite=True)
        print(f" Flux file saved: {pathFluxOut}")
       
        
        # Copy .conf file
        pathFichCopiar=os.path.join(directory,fichCopiar)
        if os.path.exists(pathFichCopiar):
            pathFichDestino=os.path.join(outDirMod, fichCopiar)
            if not os.path.exists(pathFichDestino):
                shutil.copy(pathFichCopiar, pathFichDestino)
                print(f" Conf file copied: {pathFichDestino}")
            else:
                print(f"Conf file already exists: {pathFichDestino}")
        else:
            print(f"Conf file doesn't exist: {pathFichCopiar}")
    
        pathDirConvo=os.path.join(directory, 'convolved')
        if not listInstruments:
            listInstruments=os.listdir(pathDirConvo)
        for instrumento in listInstruments:
            pathInst=os.path.join(pathDirConvo, instrumento)
            pathInstOut=os.path.join(outDirMod, 'convolved', instrumento)
            os.makedirs(pathInstOut, exist_ok=False)
            if not os.path.isdir(pathInst):
                continue
            for archivo in os.listdir(pathInst):
                if not archivo.endswith('.fits'):
                    continue
                pathArchivo=os.path.join(pathInst, archivo)
                with fits.open(pathArchivo) as hdul:
                    metaData = hdul[0].header
                    infoFilts = hdul[1].data
                    headerFilts = hdul[1].header
                    infoApert = hdul[2].data
                    headerApert = hdul[2].header
                #select only the filters of models above the MS
                filtrosAboveMS=infoFilts[np.isin(infoFilts['MODEL_NAME'], filtered_models)]
                    # Primary HDU (for metadata)
                hduFilts = fits.PrimaryHDU()
                hduFilts.header = metaData
                hduFilts.header['NMODELS'] = nModSelel
                hdu1 = fits.BinTableHDU(filtrosAboveMS, name='FLUXES')
                hdu1.data = filtrosAboveMS
                hdu1.header = headerFilts
                hdu1.header['NAXIS2']= nModSelel
                hdu2 = fits.BinTableHDU(infoApert, name='APERTURES')
                hdu2.data = infoApert
                hdu2.header = headerApert
                hdulist = fits.HDUList([hduFilts, hdu1, hdu2])
                pathFiltOut=os.path.join(pathInstOut, archivo)
                hdulist.writeto(pathFiltOut)
                print(f"Filter file saved: {pathFiltOut}")
    
       
       

def change_grid(original_zip, outDir):

    '''Zip the original model grids, extract the new family model grids to the main 
       directory and delete the new created folder

       original_zip (str): Name of the zip where original Richardson grids will be
       outDir (str): Name of the folder where new grids have been saved in filter_aboveMS
    '''

    with zipfile.ZipFile(original_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fam in directories:
    
            for file in fam.rglob("*"):                               # Write a zip file
                if file.is_file():
                    zipf.write(file, file.relative_to('.'))

            print(fam,' zipped.')
    
    
    for new_fam in outDir.iterdir():                             # Move new grids to main directory
        if new_fam.is_dir():
            shutil.move(str(new_fam), str(new_fam.name))
            
        print(new_fam,' moved to directory.')
            
    shutil.rmtree(outDir)
