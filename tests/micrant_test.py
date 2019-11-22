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
import sys

path_to_script = os.path.dirname(os.path.abspath(__file__))

def inc(x):
    return x + 1



# @pytest.mark.interactive
# # @pytest.mark.slow
# def test_answer():
#     assert inc(3) == 5


def test_just_create_object():
    mapp = micrant.micrant_app.MicrAnt()
    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    assert len(xfn) > 0

def test_just_create_object():
    qapp = QtWidgets.QApplication(sys.argv)
    mapp = micrant.micrant_app.MicrAnt()

    xfn = mapp.parameters.param("Output", "Common Spreadsheet File").value()
    mapp.start_gui(skip_exec=True, qapp=qapp)
    mapp.set_parameter("Annotation;Annotated Parameter", "SNI")
    mapp.gui_next_image()
