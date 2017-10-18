#!/usr/bin/env python3
import sys
import unittest
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath('print_lev_groups.py'))))
import print_lev_groups


class TestPrintGroups(unittest.TestCase):
    
    def test_to_graph(self):
        nodes = [['Liu Kang'], ['Noob Saibot'], ['Kung Lao']]
        relationshop_between_nodes = []
        result = print_lev_groups.to_graph(nodes)
        print_lev_groups.draw_cluster(result, print_lev_groups.list_to_dict(relationshop_between_nodes), print_lev_groups.networkx.spring_layout(result))
        print_lev_groups.plot.show()
        input('Press any ket to continue...')