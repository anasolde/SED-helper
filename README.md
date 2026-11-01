# aaaa

Python workflow for reproducible spectral energy distribution (SED) fitting and analysis using [`sedfitter`](https://github.com/richardson-t/sedfitter).

## Overview

This repository contains the Python routines developed for the analysis presented in:

> **referencia del paper**

The workflow is designed to facilitate the preparation of input data, the execution of SED fitting using `sedfitter`, and the subsequent processing, analysis, and visualization of the results.

The main workflow includes:

1. Preparation of input catalogs in the format required by `sedfitter`.
2. Filtering of the Richardson et al. (2024) YSO model grids according to the methodology described in the associated paper.
3. Configuration and execution of the SED fitting procedure.
4. Collection and processing of the fitting outputs.
5. Generation of structured result tables.
6. Analysis and visualization of the resulting physical parameters.

## Repository structure

```text
aaaa/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── THIRD_PARTY_NOTICES.md
├── requirements.txt
├── environment.yml
│
├── notebooks/
│   ├── 01_template_preparation.ipynb
│   ├── 02_input.ipynb
│   ├── 03_sed_fitting.ipynb
│   └── 04_analysis.ipynb
│
├── functions
│    ├── filter_templates.py
│    ├── KL.py
│    ├── input.py
│    ├── fitter.py
│    ├── reading.py
│    ├── result_files.py
│    ├── plots_routine.py
│    └── Packages/
│        ├── Sedfitter_main.md
│        ├── Convolve_gaia.md
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

1. Install the required Python dependencies.
2. Obtain the model grids from Zenodo.
3. Apply the model-grid filtering procedure included in this repository and convolve Gaia filters.
4. Prepare the input catalog.
5. Run the SED fitting procedure.
6. Process and analyze the resulting outputs.

Detailed installation and reproduction instructions will be provided in this repository.


## Citation

If you use this code, please cite the associated scientific publication:

> Referencia al paper

Please also cite the original publications and software associated with the third-party tools and model grids used by this workflow.

## Third-party software and model grids

This project uses external scientific software and model grids, including:

- `Sedfitter`, developed and published by Thomas P. Robitaille and collaborators.
- The updated model grids presented by Richardson et al. (2024).
- Extra functions included in Richardson et al. (2024) dataset. 
The original source code and model grids from these third-party projects are not redistributed in this repository.

The filtered model grids used in the analysis are generated locally from the original publicly available grids using the filtering routine included in this repository.

References for these works are described in `THIRD_PARTY_NOTICES` file.

## License

The custom Python code contained in this repository is distributed under the terms specified in the `LICENSE` file.

Third-party software and model grids are subject to their respective licenses and terms of use.
