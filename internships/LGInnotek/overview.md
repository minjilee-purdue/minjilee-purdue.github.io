#### Transitioning from Sequential to Parallel Processing in Manufacturing
Manufacturing companies like LG Innotek handle extremely large datasets, such as high-resolution images for camera modules or semiconductor inspection. These datasets require efficient processing methods to ensure high throughput and precision. Traditionally, sequential processing is used, where tasks are executed one after another. However, this approach can become a bottleneck when handling massive data volumes.

To overcome this, parallel processing can be implemented, where multiple tasks are executed simultaneously. The transition from sequential to parallel processing involves understanding the trade-offs between processing speed, resource utilization, and system complexity. Mathematical models like speedup calculations, Amdahl's Law, and load balancing equations help optimize this transition. Additionally, techniques such as Kullback–Leibler divergence are used to minimize discrepancies between process data and operational data, ensuring alignment and efficiency.

Below, we describe the mathematical principles underlying this transition.

##### Sequential Processing Time
Sequential processing calculates the total time by summing up the execution times of all tasks:

$$
T_{\text{sequential}} = \sum_{i=1}^{n} t_i
$$

- \( T_{\text{sequential}} \): Total processing time for sequential execution  
- \( t_i \): Time taken for task \( i \)  
- \( n \): Total number of tasks  

---

##### Parallel Processing Time

Parallel processing determines the total time by taking the maximum time among all parallel tasks:

$$
T_{\text{parallel}} = \max(t_1, t_2, \dots, t_n)
$$

- \( T_{\text{parallel}} \): Total processing time for parallel execution  
- \( t_1, t_2, \dots, t_n \): Execution times of individual tasks  

---

##### Speedup Formula

The speedup from transitioning to parallel processing is calculated as:

$$
S = \frac{T_{\text{sequential}}}{T_{\text{parallel}}}
$$

- \( S \): Speedup factor  

---

##### Amdahl's Law

Amdahl's Law estimates the theoretical maximum speedup when only a portion of tasks can be parallelized:

$$
S_{\text{speedup}} = \frac{1}{(1 - P) + \frac{P}{N}}
$$

- \( P \): Proportion of tasks that can be parallelized (\( 0 \leq P \leq 1 \))  
- \( N \): Number of parallel processors  

---

##### Load Balancing Optimization

To maximize the efficiency of parallel processing, tasks should have similar execution times:

$$
\text{Minimize} \; \left| t_i - t_j \right| \quad \forall i, j
$$

- Goal: Minimize the difference between execution times of tasks \( i \) and \( j \).  

---

##### Kullback–Leibler Divergence for Data Alignment

To ensure consistency between process data and operational data distributions:

$$
D_{\text{KL}}(P || Q) = \sum_{x \in X} P(x) \log \frac{P(x)}{Q(x)}
$$

- \( D_{\text{KL}} \): Kullback–Leibler divergence  
- \( P(x) \): Process data distribution  
- \( Q(x) \): Operational data distribution  

---

##### Key Insights

1. Sequential processing is simple but inefficient for large datasets.  
2. Parallel processing significantly improves processing speed but requires careful optimization, such as load balancing and synchronization.  
3. Amdahl's Law highlights the diminishing returns of parallelization as the proportion of sequential tasks increases.  
4. Kullback–Leibler divergence helps align process data with operational data, ensuring consistency in manufacturing workflows.
