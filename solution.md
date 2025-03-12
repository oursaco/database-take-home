
## Solution 

I spent way too long trying to get the emojis to render :(

### Iteration Journey

For my first idea, I decided to solve a simpler version of the problem, ignoring the exponential distribution. Instead, I guaranteed that every query would reach its desired node by creating a big cycle. This idea achieved a score of a bit over 200.

After running this, I notice that there are very few distinct nodes that are actually queried, so there is really no need to search over a very large cycle. Instead, we could have a small cycle consisting of the relevant nodes, and have all the unnecessary nodes feed into the cycle. This increases the score to around 470.

We can additionally optimize the previous idea, since within the few distinct queried nodes (call these important nodes), there are still differences in the amount of times they are queried. My first idea for optimizing this is to weight the number of unnecessary nodes that feeds into each important nodes by the number of times they are queried. After implementing this, it actually performs worse than the previous idea. Why?

From looking at the data, the issue is that when a path enters the cycle, it might have to loop around the entire cycle to find its target node. Thus, we should be ordering the cycle in such a way so that the expected number of steps to reach the target node is minimized once a path enters the cycle. We can do this by having every single unnecessary node feed into the most occuring queried node and have the cycle loop around in decreasing order of occurence. This improves the score to around 540.

Using this algorithm, the distribution of path lengths should be monotonically decreasing. However, there is a wierd gaps in the histogram when using the visualizer (specifically path length of 10 occurs much less than lengths 11-16). I believe this is since there is a chance for the random starting node to be within the cycle, which could then force it to loop around before reaching its target. How can we target this issue?

The main source of this issue is that the cycle length is long, but we can use a probabilistic solution to get around it. My idea was to split the important nodes into 3 cycles instead of one big cycle to reduce the cycle length.

### Approach & Analysis

My approach mainly used the observation that cycles allowed all nodes in the cycle to reach each other deterministically. Since very few nodes are acutally queried, only a small cycle is needed, and all other paths can funnel into the small cycle.

### Optimization Strategy

To optimize this approach, we mainly order the cycle such that the cycle ends up checking nodes in sorted order of occurence. This guarantees that the most likely target node is checked first, second most likely is checked second, and so on.

This strategy ends up bottlenecked by the cycle length, since if a high occuring node query starts in the cycle, it will have to loop around the entire cycle before reaching its target node. Thus, I tried to split the one big cycle into 3 cycles. Say the important nodes are sorted in order of occurence from $a_0, a_1, \ldots, a_n$ Then, the graph would look like

$a_0 \to a_1 \to a_2 \ldots a_x \to a_0$

$a_0 \to a_{x + 1} \to a_{x + 2} \ldots a_y \to a_0$

$a_0 \to a_{y + 1} \to a_{y + 2} \ldots a_n \to a_0$

Where $x$ and $y$ are some predefined constants.

The weights of $a_0 \to a_1$, $a_0 \to a_{x + 1}$ and $a_0 \to a_{y + 1}$ should be weighted to minimize expected moves. Unfortunately I didn't have enough time to improve this idea enough to outperform the previous idea, but the most recent implementation is on this commit.

### Implementation Details

Best performing code (uses first optimization idea described above):

```python
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


# create small cycle of important nodes
important_node_list = [key for key, value in important_nodes.items()]

important_node_list.sort(key = lambda x : -important_nodes[x])
print(important_node_list)

for i in range(len(important_node_list)):
    u = important_node_list[i]
    v = important_node_list[(i + 1)%len(important_node_list)]
    optimized_graph[u][v] = 1
```

### Results

The best performing code achieves a score of around 530-540. My most recent implementation achieves a score of around 510-540.

### Trade-offs & Limitations

Some limitations for my best performing code was that it is very dependent on knowing the queries beforehand since some nodes will just never be reached. It also had the issue described in the optimization section where if a path starts in the cycle, it may end up walking extra.

For my most recent implementation it still has the limitation of needing to know the queries beforehand, but it also have some tradeoffs in how to partition the important nodes into paths. Increasing the length/changing the probability of entering of one of the cycles might increase or decrease the number of walks for different starting/target nodes.

### Other Ideas

For my most recent implementation, its possible to choose cycle lengths and weights to minimize the expected number of moves. Let $l_i$ be the length of cycle $i$, $p_i$ be the probability of entering cycle $i$ from $a_0$, $pos_x$ be the position of node $x$ in its cycle, $c_x$ be $x$'s cycle, and $prob_x$ be the probability that node $x$ is queried. Then, the expected number of moves would be $1 + \sum_x prob_x(pos_x + \frac{1}{p_{c_x}}\sum_{i \neq c_x} p_i l_i)$. Then, for every combination of cycle lengths, $pos_x$ is fixed, so we could just try every possible cycle length and probability to take the minimum over all of them. Unfortunately, I didn't have time to implement this.

Another idea I didn't have time to implement would be a more generalized version of the three cycles, where more nodes other than $a_0$ is allowed to branch. This could probably be optimized to minimize expectation as well with some dynamic programming (haven't worked out any details yet).

Some more things I wanted to try but didnt't have time to:
- Sacrificing success rate for path length
- Ideas that require more probabilistic methods:
    - Making the graph strongly connected so all query can be reached
    - Other structures with smaller diameter than cycles