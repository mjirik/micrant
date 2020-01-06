  
[![Build Status](https://travis-ci.org/mjirik/micrant.svg?branch=master)](https://travis-ci.org/mjirik/micrant)
[![Coverage Status](https://coveralls.io/repos/github/mjirik/micrant/badge.svg?branch=master)](https://coveralls.io/github/mjirik/micrant?branch=master)
[![PyPI version](https://badge.fury.io/py/micrant.svg)](http://badge.fury.io/py/micrant)


# Micrant

Annotation of microscopic data for image processing by comparing two images.


![graphics](graphics/micrant_screenshot01.png)


# Install

You can use [anaconda distribution](https://docs.conda.io/en/latest/miniconda.html)
for easy installation 

```bash
conda install -c mjirik -c conda-forge -c bioconda scaffan python=3.6 pytest
```

## Get sample data and test

Download sample images to ~/data

```bash
python -m io3d.datasets -v -l CMU-1 CMU-1-annotation SCP003
python -m pytest tests/
```



