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
path_to_script = op.dirname(op.abspath(__file__))
pth = op.join(path_to_script, "../../scaffan/")
sys.path.insert(0, pth)

def inc(x):
    return x + 1


# @pytest.mark.interactive
# # @pytest.mark.slow
# def test_answer():
#     assert inc(3) == 5

TEST_XLSX = Path("test.xlsx")

global_qapp = QtWidgets.QApplication(sys.argv)


def test_just_create_object():
    mapp = micrant.micrant_app.MicrAnt()
    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    assert len(xfn) > 0


def test_just_create_object_and_set_parameter():
    mapp = micrant.micrant_app.MicrAnt()
    xfn1 = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    assert len(xfn1) > 0
    mapp.set_parameter("Output;Common Spreadsheet File", "test.xlsx")
    xfn2 = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    assert len(xfn2) > 0
    assert xfn2 != xfn1


def test_just_add_image():

    if TEST_XLSX.exists():
        os.remove(TEST_XLSX)

    mapp = micrant.micrant_app.MicrAnt()
    mapp.set_parameter("Output;Common Spreadsheet File", TEST_XLSX)
    fn = io3d.datasets.join_path(
        "medical", "orig", "sample_data", "SCP003", "SCP003.ndpi", get_root=True
    )
    mapp.set_parameter("Output;Common Spreadsheet File", TEST_XLSX)
    mapp.set_annotation_color_selection("#0000FF")
    mapp.set_input_file(fn)
    # logger.debug("")
    assert TEST_XLSX.exists()

def test_just_run_application_without_exec():
    # qapp = QtWidgets.QApplication(sys.argv)
    qapp = global_qapp
    mapp = micrant.micrant_app.MicrAnt()
    mapp.start_gui(qapp=qapp, skip_exec=True)


def test_just_create_next_image():
    # qapp = QtWidgets.QApplication(sys.argv)
    qapp = global_qapp
    mapp = micrant.micrant_app.MicrAnt()
    mapp.set_parameter("Output;Common Spreadsheet File", TEST_XLSX)

    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    logger.debug(f"Common Spreadsheet File {xfn}")
    mapp.start_gui(skip_exec=True, qapp=qapp)
    mapp.set_parameter("Annotation;Annotated Parameter", "SNI")
    mapp.set_parameter("Annotation;Lower Threshold", 0)
    mapp.set_parameter("Annotation;Upper Threshold", 2)
    logger.debug("before gui_next_image()")
    mapp.gui_left_is_lower_and_show_next()
    assert len(mapp.report.df) == 0

def test_annotation_left_right_and_set():
    qapp = global_qapp
    # qapp = QtWidgets.QApplication(sys.argv)
    mapp = micrant.micrant_app.MicrAnt()
    mapp.set_parameter("Output;Common Spreadsheet File", TEST_XLSX)

    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    logger.debug(f"Common Spreadsheet File {xfn}")
    mapp.start_gui(skip_exec=True, qapp=qapp)
    mapp.set_parameter("Annotation;Annotated Parameter", "SNI")
    mapp.set_parameter("Annotation;Lower Threshold", 0)
    mapp.set_parameter("Annotation;Upper Threshold", 2)
    logger.debug("before gui_next_image()")
    mapp.gui_left_is_lower_and_show_next()
    assert len(mapp.report.df) == 0

    mapp.gui_right_is_lower_and_show_next()
    assert len(mapp.report.df) == 2

    lrow = mapp._row1
    mapp.gui_set_left_75_percent_and_show_next()
    assert len(mapp.report.df) == 3
    assert mapp.report.df["SNI"].iat[2] == 1.5
    assert lrow["Annotation ID"] == mapp.report.df["Annotation ID"].iat[2]
    assert lrow["File Name"] == mapp.report.df["File Name"].iat[2]
