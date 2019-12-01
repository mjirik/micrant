#! /usr/bin/python
# -*- coding: utf-8 -*-

# import logging
# logger = logging.getLogger(__name__)
from loguru import logger
import pytest
import os.path
import micrant
import micrant.micrant_app
from PyQt5 import QtWidgets
import io3d
import sys
from pathlib import Path

path_to_script = os.path.dirname(os.path.abspath(__file__))


def inc(x):
    return x + 1


# @pytest.mark.interactive
# # @pytest.mark.slow
# def test_answer():
#     assert inc(3) == 5

TEST_XLSX = Path("test.xlsx")


def test_just_create_object():
    mapp = micrant.micrant_app.MicrAnt()
    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    assert len(xfn) > 0


def test_just_create_object():
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


def test_just_create_next_image():
    qapp = QtWidgets.QApplication(sys.argv)
    mapp = micrant.micrant_app.MicrAnt()
    mapp.set_parameter("Output;Common Spreadsheet File", TEST_XLSX)

    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    logger.debug(f"Common Spreadsheet File {xfn}")
    mapp.start_gui(skip_exec=True, qapp=qapp)
    mapp.set_parameter("Annotation;Annotated Parameter", "SNI")
    mapp.set_parameter("Annotation;Threshold", 2)
    mapp.gui_next_image()
