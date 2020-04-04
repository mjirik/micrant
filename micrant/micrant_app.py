# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modul is used for GUI of Lisa
"""

from loguru import logger
import sys
import os.path as op
path_to_script = op.dirname(op.abspath(__file__))
pth = op.join(path_to_script, "../../scaffan/")
sys.path.insert(0, pth)

from PyQt5 import QtGui

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QVBoxLayout,
    QSizePolicy,
    QMessageBox,
    QWidget,
    QPushButton,
)
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import scaffan
from scaffan import image
from scaffan import image_intensity_rescale_pyqtgraph
from exsu.report import Report
import sys
import datetime
from pathlib import Path
import io3d.misc
from io3d import cachefile
import micrant
# import json
# import time
import platform
from typing import List, Union
import exsu
import numpy as np
import pandas as pd

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.widgets
from . import image_sort_tools as imst
from . import couple_generator


class MicrAnt:
    def __init__(self):

        self.report: Report = Report()
        # self.report.level = 50

        self.raise_exception_if_color_not_found = False
        self.qapp = None

        # import scaffan.texture as satex
        # self.glcm_textures = satex.GLCMTextureMeasurement()
        # self.slide_segmentation = scaffan.slide_segmentation.ScanSegmentation()
        # self.slide_segmentation.report = self.report

        # self.lobulus_processing.set_report(self.report)
        # self.glcm_textures.set_report(self.report)
        # self.skeleton_analysis.set_report(self.report)
        # self.evaluation.report = self.report
        self.intensity_rescale = image_intensity_rescale_pyqtgraph.RescaleIntensityPercentilePQG(pvalue=True)
        self.win: QtGui.QWidget = None
        # self.win = None
        self.cache = cachefile.CacheFile("~/.micrant_cache.yaml")
        # self.cache.update('', path)
        common_spreadsheet_file = self.cache.get_or_save_default(
            "common_spreadsheet_file",
            self._prepare_default_output_common_spreadsheet_file(),
        )
        logger.debug(
            "common_spreadsheet_file loaded as: {}".format(common_spreadsheet_file)
        )
        params = [
            {
                "name": "Input",
                "type": "group",
                "children": [
                    {"name": "File Path", "type": "str"},
                    {"name": "Select", "type": "action"},
                    {"name": "Data Info", "type": "str", "readonly": True},
                    # {
                    #     "name": "Automatic Lobulus Selection",
                    #     "type": "bool",
                    #     "value": False,
                    #     "tip": "Skip selection based on annotation color and select lobulus based on Scan Segmentation. ",
                    # },
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
                    # {
                    #     "name": "Directory Path",
                    #     "type": "str",
                    #     "value": self._prepare_default_output_dir(),
                    # },
                    # {"name": "Select", "type": "action"},
                    {
                        "name": "Common Spreadsheet File",
                        "type": "str",
                        "value": common_spreadsheet_file,
                    },
                    {
                        "name": "Select Common Spreadsheet File",
                        "type": "action",
                        "tip": "All measurements are appended to this file in addition to data stored in Output Directory Path.",
                    },
                ],
            },
            {
                "name": "Annotation",
                "type": "group",
                "children": [
                    {"name": "Annotated Parameter", "type": "str", "value": "", "color":"#FFFF00"},
                    {"name": "Upper Threshold", "type": "float", "value": 2},
                    {"name": "Lower Threshold", "type": "float", "value": 0},
                ],
            },
            {
                "name": "Processing",
                "type": "group",
                "children": [
                    {"name": "Image Level", "type": "int", "value": 3},
                    self.intensity_rescale.parameters,
                    # {'name': 'Directory Path', 'type': 'str', 'value': prepare_default_output_dir()},
                    # {
                    #     "name": "Show",
                    #     "type": "bool",
                    #     "value": False,
                    #     "tip": "Show images",
                    # },
                    # {
                    #     "name": "Open output dir",
                    #     "type": "bool",
                    #     "value": False,
                    #     "tip": "Open system window with output dir when processing is finished",
                    # },
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
            { "name": "Left Image Annotation",
              "type": "group",
              "tip": "Direct annotation of left image",
              "children": [
                {
                    "name": "New Parameter Value",
                    "type": "float",
                    "value": 0,
                    "tip": "Used when Set Left is clicked",
                },
                {
                    "name": "Set Left",
                    "type": "action",
                    "tip": "Set parameter value of left image and show next couple",
                },
                {
                    "name": "Set Left 0%",
                    "type": "action",
                    "tip": "Set parameter value of left image and show next couple",
                },
                {
                    "name": "Set Left 25%",
                    "type": "action",
                    "tip": "Set parameter value of left image and show next couple",
                },
                {
                    "name": "Set Left 50%",
                    "type": "action",
                    "tip": "Set parameter value of left image and show next couple",
                },
                {
                    "name": "Set Left 75%",
                    "type": "action",
                    "tip": "Set parameter value of left image and show next couple",
                },
                {
                    "name": "Set Left 100%",
                    "type": "action",
                    "tip": "Set parameter value of left image and show next couple",
                },
            ]},
            { "name": "Comparative Annotation",
              "type": "group",
              "children": [
                {
                    "name": "Left is lower",
                    "type": "action",
                    "tip": "Annotated parameter on left image is lower than on right image",
                },
                {
                    "name": "Right is lower",
                    "type": "action",
                    "tip": "Annotated parameter on right image is lower than on left image",
                },
            ]},
            {"name": "Save", "type": "action"},
            # {"name": "Run", "type": "action"},
            # {'name': 'Numerical Parameter Options', 'type': 'group', 'children': [
            #     {'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True,
            #      'suffix': 'V'},
            #     {'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
            #     {'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True,
            #      'suffix': 'Hz'},
            #
            # ]},
        ]
        self.parameters = Parameter.create(name="params", type="group", children=params)
        # here is everything what should work with or without GUI
        self.parameters.param("Input", "File Path").sigValueChanged.connect(
            self._get_file_info
        )
        self.anim: image.AnnotatedImage = None
        self.image1 = None
        self.image2 = None
        self.comparison_iterator = None
        self._n_readed_regions = 0
        self._n_files = 0
        self._n_files_without_proper_color = 0
        self._right_is_lower_callback = None
        self._left_is_lower_callback = None

        self._img1 = None
        self._row1 = None
        self._img2 = None
        self._row2 = None
        # self.couple_selection_strategy = "quick"
        self.couple_selection_strategy = "bubble"

    def set_parameter(self, param_path, value, parse_path=True):
        """
        Set value to parameter.
        :param param_path: Path to parameter can be separated by ";"
        :param value:
        :param parse_path: Turn on separation of path by ";"
        :return:
        """
        logger.debug(f"Set {param_path} to {value}")
        if parse_path:
            param_path = param_path.split(";")
        fnparam = self.parameters.param(*param_path)
        fnparam.setValue(value)

    def _prepare_default_output_dir(self):
        default_dir = io3d.datasets.join_path(get_root=True)
        # default_dir = op.expanduser("~/data")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~")

        # timestamp = datetime.datetime.now().strftime("SA_%Y-%m-%d_%H:%M:%S")
        timestamp = datetime.datetime.now().strftime("MA_%Y%m%d_%H%M%S")
        default_dir = op.join(default_dir, timestamp)
        return default_dir

    def _prepare_default_output_common_spreadsheet_file(self):
        default_dir = io3d.datasets.join_path(get_root=True)
        # default_dir = op.expanduser("~/data")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~")

        # timestamp = datetime.datetime.now().strftime("SA_%Y-%m-%d_%H:%M:%S")
        # timestamp = datetime.datetime.now().strftime("SA_%Y%m%d_%H%M%S")
        default_dir = op.join(default_dir, "micrant_data.xlsx")
        return default_dir

    def _get_file_info(self):
        pass
        # fnparam = Path(self.parameters.param("Input", "File Path").value())
        # if fnparam.exists() and fnparam.is_file():
        #     anim = scaffan.image.AnnotatedImage(str(fnparam))
        #     self.parameters.param("Input", "Data Info").setValue(anim.get_file_info())

    def _show_input_files_info(self):
        msg = (
            f"Readed {self._n_readed_regions} regions from {self._n_files} files. "
            + f"{self._n_files_without_proper_color} without proper color."
        )
        logger.debug(msg)
        self.parameters.param("Input", "Data Info").setValue(msg)

    def save_data(self):
        logger.debug(self.report.df)
        self._dump_report()
        # self.report.init()
        pass

    def select_file_gui(self):
        from PyQt5 import QtWidgets

        default_dir = io3d.datasets.join_path(get_root=True)
        # default_dir = op.expanduser("~/data")
        if not op.exists(default_dir):
            default_dir = op.expanduser("~")

        filter = "NanoZoomer Digital Pathology Image(*.ndpi)"
        # fn, mask = QtWidgets.QFileDialog.getOpenFileName(
        #     self.win,
        #     "Select Input File",
        #     directory=default_dir,
        #     filter=filter
        # )

        # filter = "TXT (*.txt);;PDF (*.pdf)"
        file_name = QtGui.QFileDialog()
        file_name.setFileMode(QtGui.QFileDialog.ExistingFiles)
        names, _ = file_name.getOpenFileNames(
            self.win, "Select Input Files", directory=default_dir, filter=filter
        )
        self.set_input_files(names)

    def set_input_files(self, names):
        self._n_readed_regions = 0
        self._n_files_without_proper_color = 0
        for fn in names:
            self.set_input_file(fn)
        self._n_files = len(names)

    def set_annotation_color_selection(self, color: str):
        logger.debug(f"color={color}")
        pcolor = self.parameters.param("Input", "Annotation Color")
        color = color.upper()
        color_name = color.lower()
        color_name = color_name.capitalize()
        color_names = dict(zip(*pcolor.reverse[::-1]))
        if color_name in color_names:
            color = color_names[color_name]

        # rewrite name to code
        if color in pcolor.reverse[0]:
            # val = pcolor.reverse[0].index(color)
            # pcolor.setValue(val)
            logger.debug(f"setting color parameter to {color}")
            pcolor.setValue(color)
        else:
            raise ValueError("Color '{}' not found in allowed colors.".format(color))

    def set_input_file(self, fn: Union[Path, str]):
        fn = str(fn)
        fnparam = self.parameters.param("Input", "File Path")
        fnparam.setValue(fn)
        logger.debug("Set Input File Path to : {}".format(fn))
        self.add_ndpi_file(fn)
        self._show_input_files_info()

    def add_ndpi_file(self, filename: str):
        self.anim = image.AnnotatedImage(filename)
        self.intensity_rescale.set_anim_params(self.anim)
        # fnparam = self.parameters.param("Output", "Directory Path").value()
        fnparam = self._prepare_default_output_dir()
        self.report.init_with_output_dir(fnparam)
        logger.debug(f"report output dir: {self.report.outputdir}")
        fn_spreadsheet = self.parameters.param("Output", "Common Spreadsheet File")
        self.report.additional_spreadsheet_fn = str(fn_spreadsheet.value())

        pcolor = self.parameters.param("Input", "Annotation Color")
        color = pcolor.value()
        annotation_ids = self.anim.select_annotations_by_color(
            color, raise_exception_if_not_found=self.raise_exception_if_color_not_found
        )
        if len(annotation_ids) == 0:
            self._n_files_without_proper_color += 1
        else:
            self._n_readed_regions += 1

        for annotation_id in annotation_ids:
            inpath = Path(self.parameters.param("Input", "File Path").value())
            self.add_std_data_to_row(inpath, annotation_id)
            numeric_id = self.anim.get_annotation_id(annotation_id)
            self.report.add_cols_to_actual_row(
                {
                    "Annotation Method": "nothing",
                    "Annotation Title": self.anim.annotations[numeric_id][
                        "title"
                    ],  # [self.annotation_id]
                    "Annotation Details": self.anim.annotations[numeric_id][
                        "details"
                    ],  # [self.annotation_id]
                }
            )
            self.report.finish_actual_row()
        self._dump_report()

    def _dump_report(self):
        common_spreadsheet_file = self.parameters.param(
            "Output", "Common Spreadsheet File"
        ).value()
        excel_path = Path(common_spreadsheet_file)
        # print("we will write to excel", excel_path)
        filename = str(excel_path)
        logger.debug(f"Saving to excel file: {filename}")
        exsu.report.append_df_to_excel(filename, self.report.df)
        self.report.init()

    def add_std_data_to_row(self, inpath: Path, annotation_id):
        datarow = {}
        datarow["Annotation ID"] = annotation_id

        # self.anim.annotations.
        fn = inpath.parts[-1]
        # fn_out = self.parameters.param("Output", "Directory Path").value()
        self.report.add_cols_to_actual_row(
            {
                "File Name": str(fn),
                "File Path": str(inpath),
                "Annotation Color": self.parameters.param(
                    "Input", "Annotation Color"
                ).value(),
                "Datetime": datetime.datetime.now().isoformat(" ", "seconds"),
                "platform.system": platform.uname().system,
                "platform.node": platform.uname().node,
                "platform.processor": platform.uname().processor,
                "MicrAnt Version": micrant.__version__,
                # "Output Directory Path": str(fn_out),
            }
        )
        # self.report.add_cols_to_actual_row(self.parameters_to_dict())

        self.report.add_cols_to_actual_row(datarow)


    # def select_output_dir_gui(self):
    #     logger.debug("Deprecated call")
    #     from PyQt5 import QtWidgets
    #
    #     default_dir = self._prepare_default_output_dir()
    #     if op.exists(default_dir):
    #         start_dir = default_dir
    #     else:
    #         start_dir = op.dirname(default_dir)
    #
    #     fn = QtWidgets.QFileDialog.getExistingDirectory(
    #         None,
    #         "Select Output Directory",
    #         directory=start_dir,
    #         # filter="NanoZoomer Digital Pathology Image(*.ndpi)"
    #     )
    #     # print (fn)
    #     self.set_output_dir(fn)

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
            filter="Excel File (*.xlsx)",
        )[0]
        # print (fn)
        self.set_common_spreadsheet_file(fn)

    def set_common_spreadsheet_file(self, path):
        path = str(path)
        logger.info(" -- common_spreadsheet_file set to {}".format(path))
        fnparam = self.parameters.param("Output", "Common Spreadsheet File")
        fnparam.setValue(path)
        logger.info(" --  -- common_spreadsheet_file set to {}".format(path))
        self.cache.update("common_spreadsheet_file", path)
        # try:
        #     self.cache.update("common_spreadsheet_file", path)
        # except Exception as e:
        #     logger.debug("Problem with cache update")
        #     import traceback
        #     logger.debug(traceback.format_exc())
        logger.info("common_spreadsheet_file set to {}".format(path))

    # def gui_set_image1(self):
    #     self.image1.setPixmap(QtGui.QPixmap(logo_fn).scaled(100, 100))
    #     self.image1.show()
        # self.image2 = QtGui.QLabel()
        # self.image2.setPixmap(QtGui.QPixmap(logo_fn).scaled(100, 100))
        # self.image2.show()

    def calculate_actual_annotated_parameter(
        self, rewrite_annotated_parameter_with_recent=False, add_noise=False
    ):
        """
        Based on common spreadsheet table calculate the actual Annotated parameter
        :return:
        """
        xfn = self.parameters.param("Output", "Common Spreadsheet File").value()
        colname = self.parameters.param("Annotation", "Annotated Parameter").value()
        logger.debug(f"common spreadsheet file = {xfn}")
        logger.debug(f"Annotated Parameter = {colname}")
        if not Path(xfn).exists():
            raise FileExistsError("There is no file for processing added")
        df = pd.read_excel(xfn)
        return imst.get_new_parameter_table(
            df,
            colname,
            rewrite_annotated_parameter_with_recent=rewrite_annotated_parameter_with_recent,
            add_noise=add_noise,
        )

    def _annotated_param_and_thr_dataframe_subselection(self):
        unique_df2 = self.calculate_actual_annotated_parameter(
            rewrite_annotated_parameter_with_recent=True, add_noise=False
        )
        # self.comparison_iterator = self.generate_image_couples(df_all_with_param)
        colname = self.parameters.param("Annotation", "Annotated Parameter").value()
        upper_threshold = self.parameters.param("Annotation", "Upper Threshold").value()
        lower_threshold = self.parameters.param("Annotation", "Lower Threshold").value()
        unique_df2 = unique_df2[(unique_df2[colname] >= lower_threshold) &(unique_df2[colname] <= upper_threshold)]
        return unique_df2, colname, lower_threshold, upper_threshold

    def init_comparison(self):
        logger.debug("init comparison")
        unique_df, colname, _, _= self._annotated_param_and_thr_dataframe_subselection()
        self.unique_df = unique_df
        self.colname = colname
        ln = len(unique_df)
        couple_selection_strategy = self.couple_selection_strategy
        # method = 'quick'
        if couple_selection_strategy == "bubble":

            couple_ids = zip(range(0, ln - 1), range(1, ln))
            self.values = list(unique_df[colname])
            self.couple_generator = couple_generator.BubbleCoupleGenerator(ids=list(range(0, ln)))
            self._bubble_couple_generator = self.couple_generator
            # self.couple_id_generator = couple_ids
            self.couple_id_generator = self.couple_generator.image_couple_generator()
            self.comparison_iterator = self.show_image_couples_generator()
            self._right_is_lower_callback = self.bubble_right_is_lower_callback
            self._left_is_lower_callback = None
        elif couple_selection_strategy == "quick":
            id_array = list(range(0, len(unique_df)))
            self.couple_generator = couple_generator.QuickCoupleGenerator(id_array)
            self._quick_couple_generator = self.couple_generator
            self.couple_id_generator = self.couple_generator.image_couple_generator()
            self.comparison_iterator = self.show_image_couples_generator()
            self._right_is_lower_callback = self._quick_couple_generator.first_is_lower
            self._left_is_lower_callback = self._quick_couple_generator.first_is_higher
        else:
            raise ValueError("Unknown couple selection method")
        self._comparison_parameter_var = unique_df[colname].var()
        self._comparison_parameter_std = unique_df[colname].std()
        self._comparison_len = len(unique_df)
        self._comparison_i = 0

    def gui_show_next_image(self):

        if self.comparison_iterator is None:
            self.report.init()
            self.init_comparison()

        logger.debug(f"{self._comparison_i}/{self._comparison_len}")
        self._comparison_i += 1
        try:
            # get the next item

            row, img, prev_row, prev_img = next(self.comparison_iterator)
            self._img1 = img
            self._row1 = row
            self._img2 = prev_row
            self._row2 = prev_row

            return row, prev_row
            # self.image1.imshow(img)
            # self.image2.imshow(prev_img)
            # do something with element
        except StopIteration:
            self.comparison_iterator = None
            raise AllLobuliIterated()
            return None, None
            # if StopIteration is raised, break from loop

    def gui_left_is_lower_and_show_next(self):
        self._check_annotation_param_for_gui()
        if self._left_is_lower_callback != None:
            self._left_is_lower_callback(self._row1, self._row2)
        row, prev_row = self.gui_show_next_image()

    def gui_right_is_lower_and_show_next(self):
        self._check_annotation_param_for_gui()
        if self._right_is_lower_callback != None:
            # self._right_is_lower_callback(prev_row, prev_prev_row)
            self._right_is_lower_callback(self._row1, self._row2)
            # if output is not None:
            #     colname = self.parameters.param("Annotation", "Annotated Parameter").value()
            #     # add1 = np.random.rand() * 0.2 * (self._comparison_parameter_std)
            #     # add2 = -np.random.rand() * 0.2 * (self._comparison_parameter_std)
            #     add1 = 0.
            #     add2 = 0.
            #     left_row, right_row, multiplicator = output
            #     self._set_new_swap_value_for_first_row(
            #         left_row, right_row, colname, add_offset=add1, multiplicator=multiplicator
            #     )
            #     self._set_new_swap_value_for_first_row(
            #         right_row, left_row, colname, add_offset=add2, multiplicator=multiplicator
            #     )

        prev_row, prev_prev_row = self.gui_show_next_image()

    def bubble_right_is_lower_callback(self, left_row, right_row):
        logger.debug(f"swap 1\n{left_row}")
        logger.debug(f"swap 2\n{right_row}")
        # pokud byla minula dvojice nic
        if right_row is not None:
            colname = self.parameters.param("Annotation", "Annotated Parameter").value()
            # add1 = np.random.rand() * 0.2 * (self._comparison_parameter_std)
            # add2 = -np.random.rand() * 0.2 * (self._comparison_parameter_std)
            i, j = self._bubble_couple_generator.first_is_higher()
            add1=0.
            add2=0.
            # here we are just slightly mooving values
            multiplicator = 0.5 * np.random.rand()
            old_value1 = self.values[i]
            old_value2 = self.values[j]
            new_value1 = self._get_new_val(old_value1, old_value2, multiplicator=multiplicator)
            new_value2 = self._get_new_val(old_value2, old_value1, multiplicator=multiplicator)
            self.values[i] = new_value1
            self.values[j] = new_value2
            logger.debug(f"old and new: v1={old_value1}, {new_value1}, v2={old_value2}, {new_value2}")

            self._set_new_value_for_row(left_row, colname, new_value1, compared_row=right_row)
            self._set_new_value_for_row(right_row, colname, new_value2, compared_row=left_row)

            # Here we are swapping the values
            # multiplicator_big = 0.5 + 0.5 * np.random.rand()
            # self._set_new_swap_value_for_first_row(
            #     left_row, right_row, colname, add_offset=add1, multiplicator=multiplicator_big
            # )
            # self._set_new_swap_value_for_first_row(
            #     right_row, left_row, colname, add_offset=add2, multiplicator=multiplicator_big
            # )

    def gui_set_left_image_and_show_next(self):
        colname = self.parameters.param("Annotation", "Annotated Parameter").value()
        value = self.parameters.param("Left Image Annotation", "New Parameter Value").value()
        self.add_std_data_to_row(
            inpath=Path(self._row1["File Path"]), annotation_id=self._row1["Annotation ID"]
        )
        self.report.add_cols_to_actual_row({"Annotation Method": "set", colname: value})
        self.report.finish_actual_row()
        prev_row, prev_prev_row = self.gui_show_next_image()

    def set_left_in_percent(self, percent):
        row = self._row1

        colname = self.parameters.param("Annotation", "Annotated Parameter").value()
        upper_threshold = self.parameters.param("Annotation", "Upper Threshold").value()
        lower_threshold = self.parameters.param("Annotation", "Lower Threshold").value()

        self.add_std_data_to_row(
            inpath=Path(row["File Path"]), annotation_id=row["Annotation ID"]
        )
        value = lower_threshold + percent * 0.01 * (upper_threshold - lower_threshold)
        self.report.add_cols_to_actual_row({"Annotation Method": "set", colname: value})
        if colname in row:
            value1 = row[colname]
            self.report.add_cols_to_actual_row({"Former Annotation Parameter Value": value1})
        logger.debug(f"new val={value}, old={value1}, {Path(row['File Path']).stem}, {row['Annotation ID']}")
        self.report.finish_actual_row()

    def _check_annotation_param_for_gui(self):
        if str(self.parameters.param("Annotation", "Annotated Parameter").value()) == "":
            raise NoAnnotationParameter("Annotation Parameter required.")

    def gui_set_left_in_percent_and_show_next(self, percent):
        self._check_annotation_param_for_gui()

        self.set_left_in_percent(percent=percent)
        prev_row, prev_prev_row = self.gui_show_next_image()

    def gui_set_left_0_percent_and_show_next(self):
        self.gui_set_left_in_percent_and_show_next(0)

    def gui_set_left_25_percent_and_show_next(self):
        self.gui_set_left_in_percent_and_show_next(25)

    def gui_set_left_50_percent_and_show_next(self):
        self.gui_set_left_in_percent_and_show_next(50)

    def gui_set_left_75_percent_and_show_next(self):
        self.gui_set_left_in_percent_and_show_next(75)

    def gui_set_left_100_percent_and_show_next(self):
        self.gui_set_left_in_percent_and_show_next(100)

    def _get_new_val(self, value1, value2, add_offset=0, multiplicator=1.0):
        v1new = value1 + ((value2 - value1) * multiplicator) + add_offset
        return v1new

    def _set_new_swap_value_for_first_row(self, row, prev_row, colname, add_offset=0, multiplicator=1.0):

        value1 = row[colname]
        value2 = prev_row[colname]
        v1new = self._get_new_val(value1, value2, add_offset=add_offset,multiplicator=multiplicator)
        self._set_new_value_for_row(row, colname, v1new, prev_row)


    def _set_new_value_for_row(self, row, colname, new_value, compared_row):
        """
        Set new value and document it
        :param row:
        :param colname:
        :param new_value:
        :param compared_row:
        :return:
        """
        value1 = row[colname]
        self.add_std_data_to_row(
            inpath=Path(row["File Path"]), annotation_id=row["Annotation ID"]
        )
        logger.debug(f"new val={new_value}, old={value1}, {Path(row['File Path']).stem}, {row['Annotation ID']}")
        self.report.add_cols_to_actual_row(
            {
                # "Annotation Color": self.parameters.param(
                #     "Input", "Annotation Color"
                # ).value(),
                colname: new_value,
                "Annotation Method": "swap",
                "Former Annotation Parameter Value": value1,
            })
        # if prev_row is not None:
        if True:
            value2 = compared_row[colname]
            self.report.add_cols_to_actual_row({
                    "Compared Annotation Parameter Value": value2,
                    "Compared Annotation File Path": str(Path(compared_row["File Path"])),
                    "Compared Annotation ID": compared_row["Annotation ID"]
                }
            )
        self.report.finish_actual_row()

    # def run(self):
    #
    #     data = self.actual_row
    #     logger.debug(f"Actual row cols: {list(self.actual_row.keys())}")
    #     logger.debug(f"Persistent cols: {list(self.persistent_cols.keys())}")
    #     data.update(self.persistent_cols)
    #
    #     df = pd.DataFrame([list(data.values())], columns=list(data.keys()))
    #     logger.debug(f"Unique values types {np.unique(map(str, map(type, data.values())))}")
    #     self.df = self.df.append(df, ignore_index=True)
    def show_parameter_stats(self):
        df, colname, lower_thr, upper_thr = self._annotated_param_and_thr_dataframe_subselection()
        if len(df) < 3:
            return
        # plt.figure(self.image1.fig.number)
        # print("type: ", type(self.image1.fig))

        # plt.hist(df[colname])

        # print("df: ", df[colname])
        # ax = self.figure.add_subplot(111)
        ax = self.image1.axes
        ax.clear()
        # ax.hist(df[colname])
        # ax.plot(data, "r-")
        ax.set_title(f"Histogram of {colname}")
        ax.relim()
        ax.autoscale_view(True, True, True)
        # self.image1.draw()
        import seaborn as sns
        sns.distplot(df[colname], ax=ax, norm_hist=False)
        self.image1.draw()

        # image 2
        ax = self.image2.axes
        ax.clear()
        # ax.hist(df[colname])
        # ax.plot(data, "r-")
        ax.set_title(f"Histogram of {colname}")
        ax.relim()
        ax.autoscale_view(True, True, True)
        # self.image1.draw()
        import seaborn as sns
        print("df: ", df)
        logger.debug(f"len df: {len(df)}")
        sns.boxplot(data=df, x=colname, y="File Name", ax=ax, orient="h")
        self.image2.draw()
        # df[colname].hist(
            # ax=self.image1.axes
        # )
        # self.image1.show()

    def cache_clean(self):
        # clean cache
        logger.debug(f"cache size: {len(self.cache_ids)}")
        while len(self.cache_ids) > self.cache_size:
            self.cache_ids.pop(0)
            self.cache_data.pop(0)

    def get_row_and_image(self, row_id):
        """
        get row and image and save it to cache
        :param row_id:
        :return:
        """
        row = self.unique_df.iloc[row_id]

        ann_id = row["Annotation ID"]
        pth = row["File Path"]
        if row_id in self.cache_ids:
            img = self.cache_data[self.cache_ids.index(row_id)]
        else:
            level = self.parameters.param("Processing", "Image Level").value()
            anim = scaffan.image.AnnotatedImage(pth)
            self.intensity_rescale.set_anim_params(anim)
            img = imst.get_image_from_ann_id(anim, ann_id, level=level)
            self.cache_ids.append(row_id)
            self.cache_data.append(img)
        return row, img

    def show_image_couples_generator(self):
        """
        internally using couple id generator
        :return:
        """
        unique_df = self.unique_df
        colname = self.colname
        # anim = None
        # prev_pth = ""
        # prev_prev_row = None
        # prev_prev_img = None
        # row1 = None
        # img1 = None
        # row2 = None
        # img2 = None
        # futu_row = None
        # futu_img = None
        self.cache_size = 10
        self.cache_ids = []
        self.cache_data = []

        # ln = len(unique_df)
        # couple_ids = list(zip(range(0, ln - 1), range(1, ln)))
        # for index, row in unique_df.iterrows():
        for row_id1, row_id2 in self.couple_id_generator:  # couple_ids:

            row1, img1 = self.get_row_and_image(row_id1)
            row2, img2 = self.get_row_and_image(row_id2)
            self._img1 = img1
            self._row1 = row1
            self._img2 = img2
            self._row2 = row2

            # if prev_img is not None and actu_img is not None:
            if True:
                # TODO remove printing of values
                self.image1.axes.clear()
                self.image1.imshow(
                    img1,
                    title=f"{Path(row1['File Name']).stem}, {row1['Annotation ID']}, {self.values[row_id1]:.3}",
                )
                self.image2.axes.clear()
                self.image2.imshow(
                    img2,
                    title=f"{Path(row2['File Name']).stem}, {row2['Annotation ID']}, {self.values[row_id2]:.3}",
                )
                self.qapp.processEvents()
                logger.debug(f"left: {colname}={row1[colname]}")
                logger.debug(f"right: {colname}={row2[colname]}")
            # if hasattr(self.couple_id_generator
            for prediction_id in self.couple_generator.prediction_ids:
                # add image to cache
                self.get_row_and_image(prediction_id)

            self.cache_clean()
            yield row1, img1, row2, img2

            # if prev_pth != pth:
            #     anim = scaffan.image.AnnotatedImage(pth)
            # level = self.parameters.param("Processing", "Image Level").value()
            # prev_pth = pth
            # futu_img = imst.get_image_from_ann_id(anim, ann_id, level=level)
            # futu_row = row
            #
            # # print(f"type actu_row {type(actu_row)} prev row {type(prev_row)}")
            # logger.debug(
            #     f"next image will be: {row['File Name']}, {row['Annotation ID']}"
            # )
            # if prev_row is not None:
            #     # yield actu_row, actu_img, prev_row, prev_img
            #     yield prev_row, prev_img, prev_prev_row, prev_prev_img
            # prev_prev_row = prev_row
            # prev_prev_img = prev_img
            # prev_row = actu_row
            # prev_img = actu_img
            # actu_row = futu_row
            # actu_img = futu_img

            # print(f"ann ID={ann_id}")

    def start_gui(self, skip_exec=False, qapp=None):

        from PyQt5 import QtWidgets
        import scaffan.qtexceptionhook

        # import QApplication, QFileDialog
        if not skip_exec and qapp == None:
            qapp = QtWidgets.QApplication(sys.argv)

        self.parameters.param("Input", "Select").sigActivated.connect(
            self.select_file_gui
        )
        # self.parameters.param("Output", "Select").sigActivated.connect(
        #     self.select_output_dir_gui
        # )
        self.parameters.param(
            "Output", "Select Common Spreadsheet File"
        ).sigActivated.connect(self.select_output_spreadsheet_gui)
        self.parameters.param("Save").sigActivated.connect(self.save_data)
        self.parameters.param("Comparative Annotation", "Left is lower").sigActivated.connect(
            self.gui_left_is_lower_and_show_next
        )
        self.parameters.param("Comparative Annotation", "Right is lower").sigActivated.connect(
            self.gui_right_is_lower_and_show_next
        )
        self.parameters.param("Left Image Annotation", "Set Left").sigActivated.connect(
            self.gui_set_left_image_and_show_next
        )

        self.parameters.param("Left Image Annotation", "Set Left 0%").sigActivated.connect(
            self.gui_set_left_0_percent_and_show_next
        )

        self.parameters.param("Left Image Annotation", "Set Left 25%").sigActivated.connect(
            self.gui_set_left_25_percent_and_show_next
        )

        self.parameters.param("Left Image Annotation", "Set Left 50%").sigActivated.connect(
            self.gui_set_left_50_percent_and_show_next
        )
        self.parameters.param("Left Image Annotation", "Set Left 75%").sigActivated.connect(
            self.gui_set_left_75_percent_and_show_next
        )

        self.parameters.param("Left Image Annotation", "Set Left 100%").sigActivated.connect(
            self.gui_set_left_100_percent_and_show_next
        )
        self.parameters.param(
            "Annotation", "Annotated Parameter"
        ).sigValueChanged.connect(
            self.show_parameter_stats
        )

        # self.parameters.param("Processing", "Open output dir").setValue(True)
        t = ParameterTree()
        t.setParameters(self.parameters, showTop=False)
        t.setWindowTitle("pyqtgraph example: Parameter Tree")
        t.show()

        # print("run scaffan")
        win = QtGui.QWidget()
        win.setWindowTitle("MicrAnt {}".format(micrant.__version__))
        logo_fn = op.join(op.dirname(__file__), "micrant_icon256.png")
        app_icon = QtGui.QIcon()
        # app_icon.addFile(logo_fn, QtCore.QSize(16, 16))
        app_icon.addFile(logo_fn)
        win.setWindowIcon(app_icon)
        # qapp.setWindowIcon(app_icon)
        layout = QtGui.QGridLayout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)
        win.setLayout(layout)
        pic = QtGui.QLabel()
        pic.setPixmap(QtGui.QPixmap(logo_fn).scaled(50, 50))
        pic.show()

        self.image1 = PlotCanvas()
        self.image1.axes.set_axis_off()
        self.image1.imshow(plt.imread(logo_fn))

        # self.image1.plot()
        self.image2 = PlotCanvas()
        self.image2.axes.text(0.1, 0.6, "Set Annotation Parameter")
        self.image2.axes.text(0.1, 0.5, "Use Left Image Annotation (optimal in first iteration)")
        self.image2.axes.text(0.1, 0.4, "or")
        self.image2.axes.text(0.1, 0.3, "Use Comparative Annotation (optimal in further iterations)")
        self.image2.axes.set_axis_off()
        self.image2.draw()
        # self.image2.plot()

        # self.addToolBar(NavigationToolbar(self.image1, self))
        # self.image1.setPixmap(QtGui.QPixmap(logo_fn).scaled(100, 100))
        # self.image1.show()
        # self.image2 = QtGui.QLabel()
        # self.image2.setPixmap(QtGui.QPixmap(logo_fn).scaled(100, 100))
        # self.image2.show()
        # layout.addWidget(QtGui.QLabel("These are two views of the same data. They should always display the same values."), 0,  0, 1, 2)
        layout.addWidget(pic, 1, 0, 1, 1)
        layout.addWidget(t, 2, 0, 1, 1)
        layout.addWidget(NavigationToolbar(self.image1, win),1, 1, 1, 1)
        layout.addWidget(self.image1, 2, 1, 1, 1)
        layout.addWidget(NavigationToolbar(self.image2, win),1, 2, 1, 1)
        layout.addWidget(self.image2, 2, 2, 1, 1)
        # layout.addWidget(t2, 1, 1, 1, 1)

        win.show()
        win.resize(1600, 800)
        self.win = win
        # win.
        self.qapp = qapp
        if not skip_exec:

            qapp.exec_()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.plot()
        self.imshow_obj = None

    # not used anymore
    # def plot(self, text=None, title=None):
    #
    #     # ax = self.figure.add_subplot(111)
    #     ax = self.axes
    #     # ax = self.figure.add_subplot(111)
    #     if text is not None:
    #         ax.text(0.5, 0.5, "Set Annotation Parameter")
    #     else:
    #         data = [np.random.random() for i in range(25)]
    #         ax.plot(data, "r-")
    #     # ax.text(0.5, 0.5, "Set Annotation Parameter")
    #     if title is not None:
    #         ax.set_title("PyQt Matplotlib Example")
    #     self.draw()

    def imshow(self, *args, title="", **kwargs):
        # data = [np.random.random() for i in range(25)]
        # ax = self.figure.add_subplot(111)
        ax = self.axes
        # ax.plot(data, 'r-')
        if self.imshow_obj is None:
            self.imshow_obj = ax.imshow(*args, **kwargs)
        else:
            self.imshow_obj = ax.imshow(*args, **kwargs)
            # self.imshow_obj.set_data(args[0])
        ax.set_title(title)
        self.draw()



class AllLobuliIterated(Exception):
    pass

class NoAnnotationParameter(Exception):
    pass
