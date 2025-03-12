
## Solution 

I spent way too long trying to get the emojis to render :(

### Approach & Analysis




### Optimization Strategy

[Explain your optimization strategy in detail]

### Implementation Details

[Describe the key aspects of your implementation]

### Results

[Share the performance metrics of your solution]

### Trade-offs & Limitations

[Discuss any trade-offs or limitations of your approach]

### Iteration Journey

For my first idea, I decided to solve a simpler version of the problem, ignoring the exponential distribution. Instead, I guaranteed that every query would reach its desired node by creating a big cycle. This idea achieved a score of a bit over 200.

After running this, I notice that there are very few distinct nodes that are actually queried, so there is really no need to search over a very large cycle. Instead, we could have a small cycle consisting of the relevant nodes, and have all the unnecessary nodes feed into the cycle. This increases our score to around 470.

We can additionally optimize the previous idea, since within the few distinct queried nodes (call these important nodes), there are still differences in the amount of times they are queried. My first idea for optimizing this is to weight the number of unnecessary nodes that feeds into each important nodes by the number of times they are queried. After implementing this, it actually performs worse than the previous idea. Why?

From looking at the data, the issue is that when a path enters the cycle, it might have to loop around the entire cycle to find its target node. Thus, we should be ordering the cycle in such a way so that the expected number of steps to reach the target node is minimized once a path enters the cycle. We can do this by having every single unnecessary node feed into the most occuring queried node and have the cycle loop around in decreasing order of occurence. This improves the score slightly to 480.