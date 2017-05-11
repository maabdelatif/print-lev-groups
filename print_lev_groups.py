#!/usr/bin/env python3

import argparse
import itertools
import fileinput
import networkx
import sys
from Memoize import Memoize
from collections import namedtuple
from fuzzywuzzy import fuzz
from networkx.algorithms.components.connected import connected_components


def read_files_into_list(files):
    fields = []
    try:
        fields = [line for line in fileinput.input(files=files if files else ('-',))]
    except IOError as e:
        print('Operation failed: %s' % e)
    return fields


def to_graph(l):
    graph = networkx.Graph()
    for part in l:
        graph.add_nodes_from(part)  # each sublist is a bunch of nodes
        graph.add_edges_from(to_edges(part))  # connect nodes to each other
    return graph


def to_edges(l):
    """
        treat `l` as a Graph and returns it's edges
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    return list(zip(l[:-1], l[1:]))


def main():
    parser = argparse.ArgumentParser(description='This program prints out groups of fields that have a certain Levenshtein edit distance')

    parser.add_argument('--ratio', dest='min_match_ratio', choices=[str(i) for i in range(0,101)],
					    help='Number that determines the Levenshtein edit distance, should be between 0 and 100')
    parser.add_argument('--files', dest='files', default='', nargs='+',
					    help='The files that contains new line separated fields')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0alpha')

    opts = parser.parse_args()
    min_match_ratio = int(opts.min_match_ratio or 70)
        	
    matches = []
    field_name_and_ratio = namedtuple('Field', 'name, ratio')
    memoized_fuzz_match = Memoize(fuzz.ratio)

    fields = read_files_into_list(opts.files)
    
    for field in fields:
        ratios = [field_name_and_ratio(name=other_field, ratio=memoized_fuzz_match(field, other_field)) for other_field in fields]
        list_of_ratios_that_match_threshold = list([fld for fld in ratios if fld.ratio > min_match_ratio])
        matches.append(list_of_ratios_that_match_threshold)

    sets_of_names_that_match = [[field_in_list.name for field_in_list in list_of_fields] for list_of_fields in matches]

    # the following converts the list to a graph that will merge lists if they have shared items
    graph = to_graph(sets_of_names_that_match)
    for group in list(connected_components(graph)):
        print(group)

if __name__ == '__main__':
    main()
