# SED-helper

Helper scripts in a Python workflow for reproducible spectral energy distribution (SED) fitting and analysis using [`Sedfitter`](https://github.com/richardson-t/sedfitter), originally developed by Robitaille T. in 2017 and updated by Richardson T. in 2024. Please consult the `THIRD_PARTY_NOTICES` file for further information.


## Overview

This repository contains the Python routines developed for the analysis presented in:

> Soldevilla, A. et al. 2026, pending

The workflow is designed to facilitate the preparation of input data, the execution of SED fitting using `Sedfitter`, and the subsequent processing, analysis, and visualisation of the results.

The main workflow includes:

1. Filtering of the Richardson et al. (2024) YSO model grids according to the methodology described in the associated paper.
2. Convolving Gaia filters.
3. Preparation of input catalogues in the format required by `Sedfitter`.
4. Configuration and execution of the SED fitting procedure.
5. Collection and processing of the fitting outputs.
6. Generation of structured result tables.
7. Analysis and visualisation of the resulting physical parameters.

## Repository structure

```text
SED-helper/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── THIRD_PARTY_NOTICES.md
├── requirements.txt
│
├── notebooks/
│   ├── 01_preparation.ipynb
│   ├── 02_sed_fitting.ipynb
│   └── 03_analysis.ipynb
│
├── functions
│    ├── filt.py
│    ├── KL.py
│    ├── input_file.py
│    ├── fitter.py
│    ├── reading.py
│    ├── result_files.py
│    ├── plots_routine.py
│    └── Packages/
│        ├── Sedfitter_main.md
│        └── Template_grids.md
│
├── examples/
│    ├── YSO.csv
│    ├── Cool.csv
│    └── MS.csv
│
└── results/
    └── README.md
```


## Reproducibility

The complete workflow required to reproduce the results presented in the associated paper will be provided through a Jupyter notebook.

To reproduce the analysis, users will need to:

1. Install the required Python dependencies (instructions in `functions/Package/Sedfitter_main`).
2. Obtain the model grids from Zenodo (instructions in `functions/Package/Template_grids`).
3. Apply the model-grid filtering procedure included in this repository and convolve with Gaia filters.
4. Prepare the input catalogue.
5. Run the SED fitting procedure.
6. Process and analyse the resulting outputs.



## Citation

If you use this code, please cite the associated scientific publication:

> Soldevilla, A. et al. 2026, pending

Please also cite the original publications and software associated with the third-party tools and model grids used by this workflow.

## Third-party software and model grids

This project uses external scientific software and model grids, including:

- `Sedfitter`, developed and published by Thomas P. Robitaille and collaborators.
- The updated model grids presented by Richardson et al. (2024).
- Extra functions included in Richardson et al. (2024) dataset. 
The original source code and model grids from these third-party projects are not redistributed in this repository.

The filtered model grids used in the analysis are generated locally from the original publicly available grids using the filtering routine included in this repository.

References for these works are described in the `THIRD_PARTY_NOTICES` file.

## License

The custom Python code contained in this repository is distributed under the terms specified in the `LICENSE` file.

Third-party software and model grids are subject to their respective licenses and terms of use.
