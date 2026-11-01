import pandas as pd
import numpy as np
import os
import shutil
import tempfile
from pathlib import Path
from astropy import units as u

# Sedfitter module: https://zenodo.org/records/10522816
import sedfitter_main.sedfitter as sd
from sedfitter_main.sedfitter.sed import SEDCube
from sedfitter_main.sedfitter.extinction import Extinction


def fit_routine(fin, fout, folder_out, out_format, filters, families):

    '''Fit sedfitter routine: https://sedfitter.readthedocs.io/en/stable/api/sedfitter.fit.html#sedfitter.fit

       fin (str): name of the csv with data
       fout (str): name of the input file in the algorithm
       folder_out (str): path of the new output directory
       out_format (tuple): which fits should be output
       filters (list[str]): name of used bands as named in family folders
       families (list[str]): families to use in the fit
    '''

    data = pd.read_csv(fin)
    N= data.shape[0]
    extinction = Extinction.from_file('whitney.r550.par')

    aps = np.full(len(filters), 3.0)  # Apertures for the filters: [0.5, 22] micras
    apertures = aps * u.arcsec

    with open(fout) as main:
        for source, line in enumerate(main):

            with tempfile.TemporaryDirectory(prefix="sedfit_") as tmpdir:
                tmpdir = Path(tmpdir)

                file_input = tmpdir / f"temp_source_{source}.txt"
                file_input.write_text(line)

                star = data.loc[source]

                # -------------------------------------------------------------------
                # Distance and extinction of each source

                distance = [star.b_rgeo/1000, star.B_rgeo/1000] * u.kpc  # geometric distance from Bailer-Jones
                av = [star.b_A0, star.B_A0]          # extinction from Gaia GSP-Phot

                # -------------------------------------------------------------------

                for fam in families:
                    out_dir = tmpdir / f"result_{source+1}_{fam}"
                    out_dir.mkdir(exist_ok=True)

                    file_output = tmpdir / f"temp_file{source}_{fam}_out.fitinfo"

                    try:
                        sd.fit(str(file_input), filters, apertures, fam, str(file_output),
                               extinction_law=extinction, distance_range=distance, av_range=av,
                               output_format=out_format, output_convolved=True, remove_resolved=True)

                        sd.write_parameters(str(file_output), str(out_dir / f"best{fam}.txt"),
                                            select_format=out_format)

                        os.makedirs(folder_out+"/fitinfo", exist_ok=True)
                        shutil.copy2(file_output, Path(folder_out+"/fitinfo") / file_output.name)

                    except Exception as e:
                        print(f"Error fuente {source+1} familia {fam}")
                        print(e)

                # -------------------------------------------------------------------
                # Copy final parameter folders outside the temporary directory

                for fam in families:
                    orgn = tmpdir / f"result_{source+1}_{fam}"
                    dst = Path(f"result{source+1}_{fam}")

                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(orgn, dst)

                # At the end of this iteration, the temporary directory is deleted

    #--------------------------------------------------------------------------------------------------------
    
    # Join by families and remove temporary files and directories created in the fit
    
    for fam in families: 
        os.makedirs(folder_out+'result_'+str(fam), exist_ok=True) 
        fam_param= folder_out+'result_'+str(fam)+'/best'+str(fam)+'.txt' 

        with open(fam_param, 'a') as fout: 
            for source in range(N): 
                path= 'result'+str(source+1)+'_'+str(fam)+'/best'+str(fam)+'.txt' 
            
                with open(path,'r') as fin: 
                    if source==0: 
                        line = fin.readline() 
                    
                        while line: 
                            fout.write(line) 
                            line = fin.readline() 
                    else: 
                        for _ in range(3): # header 
                            fin.readline() 
                        line = fin.readline() 
                        
                        while line: 
                            fout.write(line) 
                            line = fin.readline() 
                            
        # remove temporary directories 
                            
        for source in range(N): 
            path= 'result'+str(source+1)+'_'+str(fam) 
            shutil.rmtree(path)
                    
                

   

    
    
    