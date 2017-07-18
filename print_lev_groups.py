#!/usr/bin/env python3

import argparse
import fileinput
import matplotlib.pyplot as plot
import networkx

import itertools

from Memoize import Memoize
from collections import namedtuple, defaultdict
from fuzzywuzzy import fuzz
from networkx.algorithms.components.connected import connected_components

field_name_and_ratio = namedtuple('Field', 'name, ratio')
memoized_fuzz_match = Memoize(fuzz.ratio)


def list_to_dict(list):
    """
        Converts a list to a dictionary
    """
    listdict = {}

    for i, item in enumerate(list):
        listdict[i] = item

    return listdict


def to_edges(l):
    """
        treat `l` as a Graph and returns it's edges
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    return list(zip(l[:-1], l[1:]))


def to_graph(l):
    """
        Converts list to a graph
    """
    graph = networkx.Graph()
    for part in l:
        graph.add_nodes_from(part)  # each sublist is a bunch of nodes
        graph.add_edges_from(to_edges(part))  # connect nodes to each other
    return graph


def draw_cluster(graph, partition, pos):
    """
        Draws interconnected clusters from a graph with the node names as labels
    """

    # Generate labels
    for node in graph.nodes():
        graph.node[node]['label'] = node

    networkx.draw_networkx_nodes(graph, pos,
                                 nodelist=graph,
                                 node_size=1000,
                                 alpha=1.0)

    networkx.draw(graph, pos)
    node_labels = networkx.get_node_attributes(graph, 'label')
    networkx.draw_networkx_labels(graph, pos, node_labels, font_size=8)


def find_matches(fields, min_match_ratio):
    """
        Find matches given a match ratio
        This is a horrible O(n^2) algorithm that needs to be optimized
    """
    fuzz_match = lambda arg1, arg2: field_name_and_ratio(name=arg2, ratio=memoized_fuzz_match(arg1, arg2))
    for field in fields:
        ratios = [fuzz_match(field, other_field) for other_field in fields]
        list_of_names_that_match_threshold = list(filter(lambda fld: fld.ratio >= min_match_ratio, ratios))
        yield list_of_names_that_match_threshold


def read_files_into_list(files):
    """
            Reads file into list (should be new line delimited text)
            If no file supplied then reads from stdin
    """
    fields = []
    try:
        fields = [line for line in fileinput.input(files=files if files else ('-',))]
    except IOError as e:
        print('Operation failed: %s' % e)
    return fields


def main():
    """
            Reads arguments, finds matches from the inputs, shows matches as groups and plots a graph
    """
    parser = argparse.ArgumentParser(description='This program prints out groups of fields that have a certain Levenshtein edit distance')

    parser.add_argument('--ratio', dest='min_match_ratio', choices=[str(i) for i in range(0,101)],
                                            help='Number that determines the Levenshtein edit distance, should be between 0 and 100')
    parser.add_argument('--files', dest='files', default='', nargs='+',
                                            help='The files that contains new line separated fields')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0alpha')

    opts = parser.parse_args()
    min_match_ratio = int(opts.min_match_ratio or 80)

    fields = read_files_into_list(opts.files)

    # the following converts the list to a graph that will merge lists if they have shared items
    matches = find_matches(fields, min_match_ratio)
    graph = to_graph([[field.name for field in fields] for fields in matches])
    draw_cluster(graph, list_to_dict([[field.ratio for field in fields] for fields in matches]), networkx.spring_layout(graph))
    for group in list(connected_components(graph)):
        print(group)

    plot.show()

if __name__ == '__main__':
    main()
