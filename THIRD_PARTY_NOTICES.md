# Third-party software and data

This repository uses external software and model grids developed and distributed by other authors. These resources are not included in this repository.

## Software

### `sedfitter`

This project uses `sedfitter`, a Python tool for fitting spectral energy distributions (SEDs), originally developed by Thomas P. Robitaille.

The version adapted for the updated YSO model grids is available here:

- Repository: https://github.com/richardson-t/sedfitter
- Original software repository: https://github.com/astrofrog/sedfitter

Please consult the respective repositories for software licensing, installation instructions, and citation requirements.

The original SED-fitting method is described in:

Robitaille, T. P., et al. (2007), *ApJS*, 169, 328.

## Model grids

This project uses the young stellar object (YSO) model grids published by Richardson et al. (2024).

- Official dataset: https://doi.org/10.5281/zenodo.10522816
- Dataset version used: Version 1.2

The original model grids and extra functions are not redistributed in this repository. Users must obtain them from the official Zenodo record and follow the dataset's terms of use.

This repository includes a Python routine to select and filter models from the original grids according to the criteria adopted in the associated scientific work. The filtered grids are generated locally and are not included here.

Reference:

Richardson, T., Ginsburg, A., Indebetouw, R., & Robitaille, T. P. (2024), *The Astrophysical Journal*, 961(2). https://doi.org/10.3847/1538-4357/ad072d

## Acknowledgment

Please cite the original software and model-grid publications when using this repository or results obtained with it. Users are responsible for checking and complying with the licensing and usage conditions of all external resources.
