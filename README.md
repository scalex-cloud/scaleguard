# Anonymous Replication Package

This repository contains the experimental data and analysis scripts required to reproduce the results reported in the submitted manuscript.

## Repository Structure

```
artifact/
│
├── data/
│   ├── experiment_summary.csv
│   └── runs/
│
├── scripts/
│
└── figures/
```

## Data

`experiment_summary.csv`

contains the metadata for all experiments included in the analysis.

The directory

```
data/runs/
```

contains the raw per-experiment CSV files.

Each filename corresponds to the `name` column in
`experiment_summary.csv`.

## Scripts

The scripts reproduce the summary statistics and figures reported in the paper.

## Requirements

Python 3

Packages:

- pandas
- numpy
- matplotlib
- seaborn