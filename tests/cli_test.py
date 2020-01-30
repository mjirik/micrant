# /usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger
import click.testing
import shutil
import pytest
import micrant.main_cli
import io3d
from pathlib import Path
import os


def test_cli():
    pth = io3d.datasets.join_path(
        "medical", "orig", "sample_data", "SCP003", "SCP003.ndpi", get_root=True
    )

    logger.debug(f"pth={pth}, exists={Path(pth).exists()}")
    common_xlsx = Path("test_data.xlsx")
    logger.debug(f"expected_pth={common_xlsx}, exists: {common_xlsx.exists()}")
    if common_xlsx.exists():
        logger.debug(f"Deleting file {common_xlsx} before tests")
        os.remove(common_xlsx)

    runner = click.testing.CliRunner()
    # runner.invoke(anwa.main_click.nogui, ["-i", str(pth)])
    runner.invoke(
        micrant.main_cli.run,
        ["nogui", "-i", pth, "-o", common_xlsx, "-c", "#0000FF"],
    )

    assert common_xlsx.exists()
