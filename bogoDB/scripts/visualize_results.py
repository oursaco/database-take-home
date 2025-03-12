#!/usr/bin/env python3
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import statistics
from collections import Counter

# Ensure scripts directory is in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

from scripts.constants import *


def visualize_query_distribution(queries_file=QUERIES_FILE):
    """
    Visualize query distribution.

    Args:
        queries_file: Path to the queries JSON file
    """
    if not os.path.exists(queries_file):
        print(f"Error: Queries file '{queries_file}' not found")
        return

    # Load queries
    with open(queries_file, "r") as f:
        queries = json.load(f)

    # Count occurrences of each target
    query_counts = Counter(queries)

    # Sort by frequency (most frequent first)
    sorted_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)

    # Print statistics
    print("Query Analysis:")
    print(f"Total queries: {len(queries)}")
    print(f"Unique targets: {len(query_counts)}")

    if sorted_queries:
        most_common = sorted_queries[0]
        print(
            f"Most frequent target: Node {most_common[0]} (queried {most_common[1]} times)"
        )

        # Calculate nodes never queried
        all_nodes = set(range(NUM_NODES))
        queried_nodes = set(int(k) for k in query_counts.keys())
        never_queried = all_nodes - queried_nodes
        print(f"Nodes never queried: {len(never_queried)}")

    # Create visualization
    plt.figure(figsize=(10, 6))

    # Plot top 20 most frequent nodes
    to_plot = sorted_queries[:20] if len(sorted_queries) > 20 else sorted_queries

    nodes = [str(q[0]) for q in to_plot]
    counts = [q[1] for q in to_plot]

    plt.bar(nodes, counts, color="blue")
    plt.xlabel("Node ID")
    plt.ylabel("Query Count")
    plt.title("Query Distribution (Top 20 most frequent targets)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save visualization
    output_file = os.path.join(project_root, "data", "query_distribution.png")
    plt.savefig(output_file)
    print(f"Query distribution saved to {output_file}")

    # Plot histogram of frequency distribution
    plt.figure(figsize=(10, 6))

    # Get all frequency values (count how many times each target was queried)
    frequencies = list(query_counts.values())

    plt.hist(frequencies, bins=min(20, len(set(frequencies))), color="orange")
    plt.xlabel("Query Frequency")
    plt.ylabel("Number of Nodes")
    plt.title("Distribution of Query Frequencies")
    plt.tight_layout()

    # Save visualization
    output_file = os.path.join(project_root, "data", "query_frequency.png")
    plt.savefig(output_file)
    print(f"Query frequency distribution saved to {output_file}")

    return query_counts


def visualize_path_distribution(results_file=OPTIMIZED_RESULTS_FILE):
    """
    Visualize path length distribution from results.

    Args:
        results_file: Path to the results JSON file
    """
    if not os.path.exists(results_file):
        print(f"Error: Results file '{results_file}' not found")
        return

    # Load results
    with open(results_file, "r") as f:
        results = json.load(f)

    # Extract path lengths
    path_lengths = []
    for result in results.get("detailed_results", []):
        if result.get("is_success", False) or result.get("success", False):
            path_length = result.get("median_path_length", float("inf"))
            if path_length != float("inf"):
                path_lengths.append(path_length)

    if not path_lengths:
        print("No successful paths found to visualize")
        return

    # Calculate statistics
    min_length = min(path_lengths)
    max_length = max(path_lengths)
    median_length = statistics.median(path_lengths)
    mean_length = sum(path_lengths) / len(path_lengths)

    print("\nPath Length Analysis:")
    print(f"Successful paths: {len(path_lengths)}")
    print(f"Range: {min_length:.1f} - {max_length:.1f}")
    print(f"Median: {median_length:.1f}")
    print(f"Mean: {mean_length:.1f}")

    # Create visualization
    plt.figure(figsize=(10, 6))

    # Create histogram
    plt.hist(path_lengths, bins=20, color="green")
    plt.xlabel("Path Length")
    plt.ylabel("Frequency")
    plt.title("Path Length Distribution")

    # Add median line
    plt.axvline(
        x=median_length,
        color="red",
        linestyle="--",
        label=f"Median: {median_length:.1f}",
    )
    plt.legend()

    plt.tight_layout()

    # Save visualization
    output_file = os.path.join(project_root, "data", "path_distribution.png")
    plt.savefig(output_file)
    print(f"Path length distribution saved to {output_file}")

    return path_lengths


if __name__ == "__main__":
    visualize_query_distribution()
    visualize_path_distribution()
