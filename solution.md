
## Solution 

I spent way too long trying to get the emojis to render :(

### Approach & Analysis

For my first idea, I decided to solve a simpler version of the problem, ignoring the exponential distribution. Instead, I guaranteed that every query would reach its desired node by creating a big cycle. This idea achieved a score of a bit over 200.

After running this, I notice that there are very few distinct nodes that are actually queried, so there is really no need to search over a very large cycle. Instead, we could have a small cycle consisting of the relevant nodes, and have all the unnecessary nodes feed into the cycle. This increases our score to around 470.


### Optimization Strategy

[Explain your optimization strategy in detail]

### Implementation Details

[Describe the key aspects of your implementation]

### Results

[Share the performance metrics of your solution]

### Trade-offs & Limitations

[Discuss any trade-offs or limitations of your approach]

### Iteration Journey

[Briefly describe your iteration process - what approaches you tried, what you learned, and how your solution evolved]

---

* Be concise but thorough - aim for 500-1000 words total
* Include specific data and metrics where relevant
* Explain your reasoning, not just what you did