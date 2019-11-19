# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modul is used for GUI of Lisa
"""
import os.path as op
import sys
path_to_script = op.dirname(op.abspath(__file__))
pth = op.join(path_to_script, "../../scaffan/")
sys.path.insert(0, pth)

from loguru import logger

from PyQt5 import QtGui
import scaffan
from scaffan import image
from exsu.report import Report
import sys
import os.path as op
import datetime
from pathlib import Path
import io3d.misc
from io3d import cachefile
import json
import time
import platform
from typing import List, Union

from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.widgets

class MicrAnt:
    def __init__(self):

        self.report: Report = Report()
        # self.report.level = 50

        self.raise_exception_if_color_not_found = True

        import scaffan.texture as satex
        # self.glcm_textures = satex.GLCMTextureMeasurement()
        # self.lobulus_processing = scaffan.lobulus.Lobulus(ptype="bool")
        # self.skeleton_analysis = scaffan.skeleton_analysis.SkeletonAnalysis()
        # self.evaluation = scaffan.evaluation.Evaluation()
        # self.slide_segmentation = scaffan.slide_segmentation.ScanSegmentation()
        # self.slide_segmentation.report = self.report

        # self.lobulus_processing.set_report(self.report)
        # self.glcm_textures.set_report(self.report)
        # self.skeleton_analysis.set_report(self.report)
        # self.evaluation.report = self.report
        self.win:QtGui.QWidget = None
        # self.win = None
        self.cache = cachefile.CacheFile("~/.micrant_cache.yaml")
        # self.cache.update('', path)
        common_spreadsheet_file = self.cache.get_or_save_default(
            "common_spreadsheet_file", self._prepare_default_output_common_spreadsheet_file())
        logger.debug("common_spreadsheet_file loaded as: {}".format(common_spreadsheet_file))
        params = [
            {
                "name": "Input",
                "type": "group",
                "children": [
                    {"name": "File Path", "type": "str"},
                    {"name": "Select", "type": "action"},
                    {"name": "Data Info", "type": "str", "readonly": True},
                    {
                        "name": "Automatic Lobulus Selection",
                        "type": "bool",
                        "value": False,
                        "tip": "Skip selection based on annotation color and select lobulus based on Scan Segmentation. ",
                    },
                    {
                        "name": "Annotation Color",
                        "type": "list",
                        "tip": "Select lobulus based on annotation color. Skipped if Automatic Lobulus Selection is used.",
                        "values": {
                            "None": None,
                            "White": "#FFFFFF",
                            "Black": "#000000",
                            "Red": "#FF0000",
                            "Green": "#00FF00",
                            "Blue": "#0000FF",
                            "Cyan": "#00FFFF",
                            "Magenta": "#FF00FF",
                            "Yellow": "#FFFF00",
                        },
                        "value": 0,
                    },
                    # {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
                    # {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
                    # BatchFileProcessingParameter(
                    #     name="Batch processing", children=[]
                    # ),
                    # {
                    #     "name": "Advanced",
                    #     "type": "group",
                    #     "children": [
                    #         dict(name="Ignore not found color",type="bool", value=False,
                    #              tip="No exception thrown if color not found in the data"),
                    #     ]
                    # }
                ],
            },
            {
                "name": "Output",
                "type": "group",
                "children": [
                    {
                        "name": "Directory Path",
                        "type": "str",
                        "value": self._prepare_default_output_dir(),
                    },
                    {"name": "Select", "type": "action"},
                    {
                        "name": "Common Spreadsheet File",
                        "type": "str",
                        "value": common_spreadsheet_file,
                    },
                    {"name": "Select Common Spreadsheet File", "type": "action",
                     "tip": "All measurements are appended to this file in addition to data stored in Output Directory Path."
                     },
                ],
            },
            {
                "name": "Processing",
                "type": "group",
                "children": [
                    # {'name': 'Directory Path', 'type': 'str', 'value': prepare_default_output_dir()},
                    {
                        "name": "Show",
                        "type": "bool",
                        "value": False,
                        "tip": "Show images",
                    },
                    {
                        "name": "Open output dir",
                        "type": "bool",
                        "value": False,
                        "tip": "Open system window with output dir when processing is finished",
                    },
                    # {
                    #     "name": "Run Scan Segmentation",
                    #     "type": "bool",
                    #     "value": True,
                    #     "tip": "Run analysis of whole slide before all other processing is perfomed",
                    # },
                    # {
                    #     "name": "Skeleton Analysis",
                    #     "type": "bool",
                    #     "value": True,
                    #     # "tip": "Show images",
                    # },
                    # {
                    #     "name": "Texture Analysis",
                    #     "type": "bool",
                    #     "value": True,
                    #     # "tip": "Show images",
                    # },
                    # self.slide_segmentation.parameters,
                    # self.lobulus_processing.parameters,
                    # self.skeleton_analysis.parameters,
                    # self.glcm_textures.parameters,
                    {
                        "name": "Report Level",
                        "type": "int",
                        "value": 50,
                        "tip": "Control ammount of stored images. 0 - all debug imagess will be stored. "
                               "100 - just important images will be saved.",
                    },
                ],
            },
            {"name": "Run", "type": "action"},
        ]
        self.parameters = Parameter.create(name="params", type="group", children=params)
        # here is everything what should work with or without GUI
        self.parameters.param("Input", "File Path").sigValueChanged.connect(
            self._get_file_info
        )
        self.anim: image.AnnotatedImage = None
        pass


    def _prepare_default_output_dir(self):
        default_dir = io3d.datasets.join_path(get_root=True)
        # default_dir = op.expanduser("~/data")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~")

        # timestamp = datetime.datetime.now().strftime("SA_%Y-%m-%d_%H:%M:%S")
        timestamp = datetime.datetime.now().strftime("SA_%Y%m%d_%H%M%S")
        default_dir = op.join(default_dir, timestamp)
        return default_dir

    def _prepare_default_output_common_spreadsheet_file(self):
        default_dir = io3d.datasets.join_path(get_root=True)
        # default_dir = op.expanduser("~/data")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~")

        # timestamp = datetime.datetime.now().strftime("SA_%Y-%m-%d_%H:%M:%S")
        # timestamp = datetime.datetime.now().strftime("SA_%Y%m%d_%H%M%S")
        default_dir = op.join(default_dir, "SA_data.xlsx")
        return default_dir

    def _get_file_info(self):
        fnparam = Path(self.parameters.param("Input", "File Path").value())
        if fnparam.exists() and fnparam.is_file():
            anim = scaffan.image.AnnotatedImage(str(fnparam))
            self.parameters.param("Input", "Data Info").setValue(anim.get_file_info())
    def run_lobuluses(self):
        pass

    def select_file_gui(self):
        from PyQt5 import QtWidgets

        default_dir = io3d.datasets.join_path(get_root=True)
        # default_dir = op.expanduser("~/data")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~")

        fn, mask = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select Input File",
            directory=default_dir,
            filter="NanoZoomer Digital Pathology Image(*.ndpi)",
        )
        self.set_input_file(fn)

    def select_output_dir_gui(self):
        from PyQt5 import QtWidgets

        default_dir = self._prepare_default_output_dir()
        if op.exists(default_dir):
            start_dir = default_dir
        else:
            start_dir = op.dirname(default_dir)

        fn = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Select Output Directory",
            directory=start_dir,
            # filter="NanoZoomer Digital Pathology Image(*.ndpi)"
        )
        # print (fn)
        self.set_output_dir(fn)

    def select_output_spreadsheet_gui(self):
        from PyQt5 import QtWidgets

        default_dir = self._prepare_default_output_dir()
        if op.exists(default_dir):
            start_dir = default_dir
        else:
            start_dir = op.dirname(default_dir)

        fn = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Select Common Spreadsheet File",
            directory=start_dir,
            filter="Excel File (*.xlsx)"
        )[0]
        # print (fn)
        self.set_common_spreadsheet_file(fn)


    def start_gui(self, skip_exec=False, qapp=None):

        from PyQt5 import QtWidgets
        import scaffan.qtexceptionhook

        # import QApplication, QFileDialog
        if not skip_exec and qapp == None:
            qapp = QtWidgets.QApplication(sys.argv)

        self.parameters.param("Input", "Select").sigActivated.connect(
            self.select_file_gui
        )
        self.parameters.param("Output", "Select").sigActivated.connect(
            self.select_output_dir_gui
        )
        self.parameters.param("Output", "Select Common Spreadsheet File").sigActivated.connect(
            self.select_output_spreadsheet_gui
        )
        self.parameters.param("Run").sigActivated.connect(
            self.run_lobuluses
        )

        self.parameters.param("Processing", "Open output dir").setValue(True)
        t = ParameterTree()
        t.setParameters(self.parameters, showTop=False)
        t.setWindowTitle("pyqtgraph example: Parameter Tree")
        t.show()

        # print("run scaffan")
        win = QtGui.QWidget()
        win.setWindowTitle("ScaffAn {}".format(scaffan.__version__))
        logo_fn = op.join(op.dirname(__file__), "scaffan_icon256.png")
        app_icon = QtGui.QIcon()
        # app_icon.addFile(logo_fn, QtCore.QSize(16, 16))
        app_icon.addFile(logo_fn)
        win.setWindowIcon(app_icon)
        # qapp.setWindowIcon(app_icon)
        layout = QtGui.QGridLayout()
        win.setLayout(layout)
        pic = QtGui.QLabel()
        pic.setPixmap(QtGui.QPixmap(logo_fn).scaled(100, 100))
        pic.show()
        # layout.addWidget(QtGui.QLabel("These are two views of the same data. They should always display the same values."), 0,  0, 1, 2)
        layout.addWidget(pic, 1, 0, 1, 1)
        layout.addWidget(t, 2, 0, 1, 1)
        # layout.addWidget(t2, 1, 1, 1, 1)

        win.show()
        win.resize(800, 800)
        self.win = win
        # win.
        if not skip_exec:

            qapp.exec_()
