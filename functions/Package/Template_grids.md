# **Template grids**

`Sedfitter` needs a grid of models of young objects (YSOs) with to fit the photometric observations. 
The templates used in this work are the updated models from Richardson T. (2024) available in Zenodo: [Richardson models](https://zenodo.org/records/10522816).

This is an update of the Robitaille, T. (2017) set of models: [astrofrog/sedfitter models](https://zenodo.org/records/21764259) in parameter space and it also retrieves additional information of the models, as well as includes some useful Python functions. 

Whole dataset includes a .tar for each family / model set, and a file.tar with a bunch of useful functions and files, and a user_filters.tar. 
When unzip the families directories, you will find something like this:

     |-- family/
         |-- r+24_models-1.2/
             |-- family/
                 |-- convolved/
                 |-- info.fits
                 |-- models.conf
                    ....

We maintain the inner `family` directory and everything inside (parent `family` and `r+24_models` can be discarded). They should be in `functions` directory. 

When unzip the files.tar, you will find:

     |-- files/
         |-- r+24_models-1.2/
             |-- glossary.txt
             |-- convolution.py
                 ....
                 
Only the inside files are required in our `functions` directory (`files` parent and `r+24_models` folders can be discarded). 

`user_filters.tar` is not necessary for our workflow.  


Please cite the original dataset publications when using this repository or results obtained with it. 
Users are responsible for checking and complying with the licensing and usage conditions of all external resources.


