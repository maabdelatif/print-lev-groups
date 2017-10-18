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

memoized_fuzz_match = Memoize(fuzz.ratio)


def to_edges(l):
    """
        treat `l` as a Graph and returns it's edges
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    return list(zip(l[:-1], l[1:]))


def to_graph(l):
    """
        Converts list to graph
    """
    graph = networkx.Graph()
    for part in l:
        graph.add_nodes_from(part)  # each sublist is a bunch of nodes
        graph.add_edges_from(to_edges(part))  # connect nodes to each other
    return graph


def draw_cluster(graph, pos):
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

    node_labels = networkx.get_node_attributes(graph, 'label')
    networkx.draw_networkx_labels(graph, pos, node_labels, font_size=8)
    networkx.draw_networkx_edges(graph, pos, edge_list=graph.edges, arrows=False)


def find_matches(words, min_match_ratio):
    """
        Find matches given a match ratio
        This is a horrible O(n^2) algorithm that needs to be optimized
        Returns the list of couples that are match the ratio threshold
    """
    fuzz_match = lambda arg1, arg2: memoized_fuzz_match(arg1, arg2)
    couples = []
    for word, paired_word in itertools.combinations(words, 2):
        ratio = fuzz_match(word, paired_word)
        if ratio >= min_match_ratio:
            couples.append([word, paired_word])
    return couples

def read_files_into_list(files):
    """
            Reads file into list (should be new line delimited text)
            If no file supplied then reads from stdin
    """
    fields = []
    try:
        fields = [line.strip() for line in fileinput.input(files=files if files else ('-',))]
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

    words = read_files_into_list(opts.files)

    # the following converts the list to a graph that will merge lists if they have shared items
    matches = find_matches(words, min_match_ratio)
    graph = to_graph(matches)
    draw_cluster(graph, networkx.spring_layout(graph))
    for group in list(connected_components(graph)):
        print(group)

    plot.show()
    input('Press any key to continue...')

if __name__ == '__main__':
    main()
