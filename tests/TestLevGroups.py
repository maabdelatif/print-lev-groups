#!/usr/bin/env python3
import sys
import unittest
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath('print_lev_groups.py'))))
import print_lev_groups


class TestPrintGroups(unittest.TestCase):
    
    def test_to_graph(self):
        list  = [['Liu Kang'], ['Noob Saibot'], ['Kung Lao']]
        result = print_lev_groups.to_graph(list)
