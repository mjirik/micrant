#! /usr/bin/python
# -*- coding: utf-8 -*-

# import logging
# logger = logging.getLogger(__name__)
from loguru import logger
from micrant import timsort

# def test_timsort():
#     cg = timsort.TimCoupleGenerator()
#
#     for couple in cg.timsort([5,6,8, 1, 3]):
#         i1, i2 = couple
#         print(f"i1: {i1}, i2: {i2}")
#         if i1 < i2:
#             cg.left_is_lower = True
#         else:
#             cg.left_is_lower = False
#
#
#     print(list(cg.sorted_array))
#
#     for items in zip(cg.sorted_array, [1,3,5,6,7]):
#         i1, i2 = items
#         assert i1 == i2


