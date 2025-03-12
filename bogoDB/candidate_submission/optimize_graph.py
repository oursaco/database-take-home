#!/usr/bin/env python3
import json
import os
import sys
import random
import numpy as np
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any

# Add project root to path to import scripts
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import constants
from scripts.constants import (
    NUM_NODES,
    MAX_EDGES_PER_NODE,
    MAX_TOTAL_EDGES,
)


def load_graph(graph_file):
    """Load graph from a JSON file."""
    with open(graph_file, "r") as f:
        return json.load(f)


def load_results(results_file):
    """Load query results from a JSON file."""
    with open(results_file, "r") as f:
        return json.load(f)


def save_graph(graph, output_file):
    """Save graph to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(graph, f, indent=2)


def verify_constraints(graph, max_edges_per_node, max_total_edges):
    """Verify that the graph meets all constraints."""
    # Check total edges
    total_edges = sum(len(edges) for edges in graph.values())
    if total_edges > max_total_edges:
        print(
            f"WARNING: Graph has {total_edges} edges, exceeding limit of {max_total_edges}"
        )
        return False

    # Check max edges per node
    max_node_edges = max(len(edges) for edges in graph.values())
    if max_node_edges > max_edges_per_node:
        print(
            f"WARNING: A node has {max_node_edges} edges, exceeding limit of {max_edges_per_node}"
        )
        return False

    # Check all nodes are present
    if len(graph) != NUM_NODES:
        print(f"WARNING: Graph has {len(graph)} nodes, should have {NUM_NODES}")
        return False

    # Check edge weights are valid (between 0 and 10)
    for node, edges in graph.items():
        for target, weight in edges.items():
            if weight <= 0 or weight > 10:
                print(f"WARNING: Edge {node} -> {target} has invalid weight {weight}")
                return False

    return True


def optimize_graph(
    initial_graph,
    results,
    num_nodes=NUM_NODES,
    max_total_edges=int(MAX_TOTAL_EDGES),
    max_edges_per_node=MAX_EDGES_PER_NODE,
):
    """
    Optimize the graph to improve random walk query performance.

    Args:
        initial_graph: Initial graph adjacency list
        results: Results from queries on the initial graph
        num_nodes: Number of nodes in the graph
        max_total_edges: Maximum total edges allowed
        max_edges_per_node: Maximum edges per node

    Returns:
        Optimized graph
    """
    print("Starting graph optimization...")

    # =============================================================
    # TODO: Implement your optimization strategy here
    # =============================================================
    #
    # Your goal is to optimize the graph structure to:
    # 1. Increase the success rate of queries
    # 2. Minimize the path length for successful queries
    #
    # You have access to:
    # - initial_graph: The current graph structure
    # - results: The results of running queries on the initial graph
    #
    # Query results contain:
    # - Each query's target node
    # - Whether the query was successful
    # - The path taken during the random walk
    #
    # Remember the constraints:
    # - max_total_edges: Maximum number of edges in the graph
    # - max_edges_per_node: Maximum edges per node
    # - All nodes must remain in the graph
    # - Edge weights must be positive and ≤ 10

    # ---------------------------------------------------------------
    # EXAMPLE: Simple strategy to meet edge count constraint
    # This is just a basic example - you should implement a more
    # sophisticated strategy based on query analysis!
    # ---------------------------------------------------------------

    # gets nodes that were queried
    important_nodes = {}
    total_queries = 0

    for res in results['detailed_results']:
        node = str(res['target'])
        if not node in important_nodes:
            important_nodes[node] = 0
        important_nodes[node] += 1
        total_queries += 1

    # initialize optimized graph
    optimized_graph = {}

    for node, edges in initial_graph.items():
        optimized_graph[node] = dict()
    
    # create list of unnecessary nodes
    unnecessary_node_list = []

    for node, edges in initial_graph.items():
        if not node in important_nodes:
            unnecessary_node_list.append(node)

    # order nodes by occurence
    important_node_list = [key for key, value in important_nodes.items()]
    important_node_list.sort(key = lambda x : -important_nodes[x])

    # split important nodes into 3 chains, ignoring most occuring node

    chain_lengths = [len(important_node_list)//2, len(important_node_list)//4]

    chains = [[], [], []]

    for i in range(1, chain_lengths[0]):
        chains[0].append(important_node_list[i])
    for i in range(chain_lengths[0], chain_lengths[0] + chain_lengths[1]):
        chains[1].append(important_node_list[i])
    for i in range(chain_lengths[0] + chain_lengths[1], len(important_node_list)):
        chains[2].append(important_node_list[i])

    # add edges for each chain and link the end to most occuring node
    for i in range(3):
        print(chains[i])
        for j in range(len(chains[i]) - 1):
            u = chains[i][j]
            v = chains[i][j + 1]
            optimized_graph[u][v] = 1
        optimized_graph[chains[i][-1]][important_node_list[0]] = 1

    # add edges from most occuring nodes to chains, should be weighted
    optimized_graph[important_node_list[0]][chains[0][0]] = 10
    optimized_graph[important_node_list[0]][chains[1][0]] = 1
    optimized_graph[important_node_list[0]][chains[2][0]] = 1

    # feed all unnecessary nodes into most important node
    for i in unnecessary_node_list:
        optimized_graph[i][important_node_list[0]] = 1
    
    # =============================================================
    # End of your implementation
    # =============================================================

    # Verify constraints
    if not verify_constraints(optimized_graph, max_edges_per_node, max_total_edges):
        print("WARNING: Your optimized graph does not meet the constraints!")
        print("The evaluation script will reject it. Please fix the issues.")

    return optimized_graph


if __name__ == "__main__":
    # Get file paths
    initial_graph_file = os.path.join(project_dir, "data", "initial_graph.json")
    results_file = os.path.join(project_dir, "data", "initial_results.json")
    output_file = os.path.join(
        project_dir, "candidate_submission", "optimized_graph.json"
    )

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Loading initial graph from {initial_graph_file}")
    initial_graph = load_graph(initial_graph_file)

    print(f"Loading query results from {results_file}")
    results = load_results(results_file)

    print("Optimizing graph...")
    optimized_graph = optimize_graph(initial_graph, results)

    print(f"Saving optimized graph to {output_file}")
    save_graph(optimized_graph, output_file)

    print("Done! Optimized graph has been saved.")
