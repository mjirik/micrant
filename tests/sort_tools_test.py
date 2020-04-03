#! /usr/bin/python
# -*- coding: utf-8 -*-

# import logging
# logger = logging.getLogger(__name__)
from loguru import logger
import pytest
import micrant
import micrant.micrant_app
from PyQt5 import QtWidgets
import io3d
from pathlib import Path
import os
import sys
import os.path as op
import pandas as pd
path_to_script = op.dirname(op.abspath(__file__))
pth = op.join(path_to_script, "../../scaffan/")
sys.path.insert(0, pth)

from micrant import image_sort_tools as imst

def test_parameter_extraction():
    default_dir = io3d.datasets.join_path(get_root=True)
    # default_dir = op.expanduser("~/data")
    if not op.exists(default_dir):
        default_dir = op.expanduser("~")

    # timestamp = datetime.datetime.now().strftime("SA_%Y-%m-%d_%H:%M:%S")
    # timestamp = datetime.datetime.now().strftime("SA_%Y%m%d_%H%M%S")
    default_dir = op.join(default_dir, "micrant_data.xlsx")
    df = pd.read_excel(default_dir)


    dfnew = imst.get_new_parameter_table(
        df,
        "SNI",
        rewrite_annotated_parameter_with_recent=True,
        add_noise=False,
    )
    print(dfnew[["SNI", "Annotation ID"]])
    assert False
