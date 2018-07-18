#!/usr/bin/env python3

"""
    Groups words according to a basic fuzzy matching ratio and graphs the result
"""

import argparse
import fileinput
import itertools
import multiprocessing as mp
from multiprocessing import Pool
import matplotlib.pyplot as plot
from fuzzywuzzy import fuzz
import networkx
from networkx.algorithms.components.connected import connected_components
from memoize import Memoize

MEMOIZED_FUZZ_MATCH = Memoize(fuzz.ratio)


def get_fuzz_ratio(first_word, second_word):
    """
        Returns the fuzzy matching ratio between two arguments
    """
    return fuzz.ratio(first_word, second_word), first_word, second_word


def to_edges(graph):
    """
        treat graph as a Graph and returns it's edges
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    return list(zip(graph[:-1], graph[1:]))


def to_graph(lst):
    """
        Converts list to graph
    """
    graph = networkx.Graph()
    for part in lst:
        graph.add_nodes_from(part)  # each sublist is a bunch of nodes
        graph.add_edges_from(to_edges(part))  # connect nodes to each other
    return graph


def draw_cluster(graph, layout):
    """
        Draws interconnected clusters from a graph with the node names as labels
    """

    # Generate labels
    for node in graph.nodes():
        graph.node[node]['label'] = node

    node_labels = networkx.get_node_attributes(graph, 'label')

    networkx.draw_networkx_nodes(
        graph, layout, nodelist=graph, node_size=1000, alpha=1.0)
    networkx.draw_networkx_labels(
        graph, layout, labels=node_labels, font_size=8)
    networkx.draw_networkx_edges(
        graph, layout, edge_list=graph.edges, arrows=False)


def find_matches(words, min_match_ratio):
    """
        Find matches given a match ratio
        This method is very slow for a large number of words - hopefully multiprocessing helps
        Returns the list of couples that match the ratio threshold
    """
    couples = []
    with Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            get_fuzz_ratio, itertools.combinations(words, 2))
    for result, word, paired_word in results:
        if result >= min_match_ratio:
            couples.append([word, paired_word])
    return couples


def read_files_into_list(files):
    """
        Reads file into list (should be new line delimited text)
        If no file supplied then reads from stdin
    """
    contents = []
    try:
        contents = [line.strip() for line in fileinput.input(
            files=files if files else ('-',))]
    except IOError as error:
        print('Operation failed: %s' % error)
    return contents


def main():
    """
        Reads arguments, finds matches from the inputs, shows matches as groups
        and plots a graph
    """
    parser = argparse.ArgumentParser(
        description='This program prints out groups of words that have a certain' \
         ' Levenshtein edit distance')

    parser.add_argument(
        '--ratio',
        dest='min_match_ratio',
        choices=[str(i) for i in range(0, 101)],
        help='Number that determines the Levenshtein edit distance, should be between 0 and 100'
    )
    parser.add_argument(
        '--files',
        dest='files',
        default='',
        nargs='+',
        help='The files that contains new line separated words'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0alpha'
    )

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
    input('Press enter to continue...')


if __name__ == '__main__':
    main()
