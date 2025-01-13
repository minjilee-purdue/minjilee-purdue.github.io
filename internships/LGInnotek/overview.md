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
5. 

##### Evaluating Sequential vs Parallel Pipelines Using KL Divergence

This document explains how to use **Kullback–Leibler (KL) Divergence** to evaluate the performance of sequential and parallel processing pipelines in manufacturing environments. The comparison is based on how closely each pipeline’s output aligns with a reference dataset (ground truth).

---

##### Scenario
In manufacturing, pipelines are used to process input data (e.g., RGB images for defect detection). These pipelines can be configured in two ways:
1. **Sequential Pipeline**: Processes tasks one at a time in sequence.
2. **Parallel Pipeline**: Processes multiple tasks simultaneously.

The goal is to evaluate which pipeline generates results closer to the reference data by calculating the KL Divergence between:
- **Reference Data (Ground Truth)**: \( Q(x) \)
- **Pipeline Outputs**:
  - Sequential: \( P_{\text{sequential}}(x) \)
  - Parallel: \( P_{\text{parallel}}(x) \)

---

##### Evaluation Steps

###### 1. Reference Data (\( Q(x) \))
The reference data represents the ideal or actual probability distribution. For example:
- \( Q(x) = \{0.8 \, (\text{defective}), 0.2 \, (\text{normal})\} \)

###### 2. Pipeline Outputs
The pipelines generate predicted probability distributions:
- Sequential Pipeline Output: \( P_{\text{sequential}}(x) = \{0.7 \, (\text{defective}), 0.3 \, (\text{normal})\} \)
- Parallel Pipeline Output: \( P_{\text{parallel}}(x) = \{0.85 \, (\text{defective}), 0.15 \, (\text{normal})\} \)

###### 3. KL Divergence Formula
The KL Divergence is calculated for each pipeline:

**For Sequential Pipeline**:
\[
D_{\text{KL}}(Q || P_{\text{sequential}}) = \sum_{x} Q(x) \log \frac{Q(x)}{P_{\text{sequential}}(x)}
\]

**For Parallel Pipeline**:
\[
D_{\text{KL}}(Q || P_{\text{parallel}}) = \sum_{x} Q(x) \log \frac{Q(x)}{P_{\text{parallel}}(x)}
\]

###### 4. Calculation Example
Let’s compute the KL Divergence for both pipelines:

###### Sequential Pipeline:
\[
D_{\text{KL}}(Q || P_{\text{sequential}}) = 0.8 \cdot \log \frac{0.8}{0.7} + 0.2 \cdot \log \frac{0.2}{0.3}
\]
Result: \( D_{\text{KL}}(Q || P_{\text{sequential}}) \approx 0.091 \)

###### Parallel Pipeline:

\[
D_{\text{KL}}(Q || P_{\text{parallel}}) = 0.8 \cdot \log \frac{0.8}{0.85} + 0.2 \cdot \log \frac{0.2}{0.15}
\]
Result: \( D_{\text{KL}}(Q || P_{\text{parallel}}) \approx 0.061 \)

---

##### Interpretation of Results

- **Sequential Pipeline**: KL Divergence = 0.091  
- **Parallel Pipeline**: KL Divergence = 0.061  

Since the KL Divergence for the parallel pipeline is smaller, it means the parallel pipeline's output aligns more closely with the reference data than the sequential pipeline.
