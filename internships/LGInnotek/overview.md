#### Transitioning from Sequential to Parallel Processing in Manufacturing
Electronic component manufacturing companies like [LG Innotek](https://www.lginnotek.com/main/main.do) handle extremely large datasets, such as high-resolution images for camera modules or semiconductor inspection. These datasets require efficient processing methods to ensure high throughput and precision. Traditionally, sequential processing is used, where tasks are executed one after another. However, this approach can become a bottleneck when handling massive data volumes.

To overcome this, parallel processing can be implemented, where multiple tasks are executed simultaneously. The transition from sequential to parallel processing involves understanding the trade-offs between **processing speed**, **resource utilization**, and **system complexity**. Mathematical models like speedup calculations, and load balancing equations help optimize this transition. Additionally, techniques such as Kullback–Leibler divergence are used to minimize discrepancies between process data and operational data, ensuring alignment and efficiency.

---

##### Sequential Processing Time
Sequential processing calculates the total time by summing up the execution times of all tasks:

$$
T_{\text{sequential}} = \sum_{i=1}^{n} t_i
$$

Where:

- $T_{\text{sequential}}$ represents the total processing time for sequential execution  
- $t_i$ represents the execution time for task $i$  
- $n$ represents the total number of tasks  

---

##### Parallel Processing Time

Parallel processing determines the total time by taking the maximum time among all parallel tasks:

$$
T_{\text{parallel}} = \max(t_1, t_2, \dots, t_n)
$$

Where:

- $T_{\text{parallel}}$ represents the total processing time for parallel execution
- $t_1, t_2, \dots, t_n$ represent execution times of individual tasks

---

##### Speedup Formula

The speedup from transitioning to parallel processing is calculated as:

$$
S = \frac{T_{\text{sequential}}}{T_{\text{parallel}}}
$$

Where:

- $S$ represents the speedup factor

---

##### Output Accuracy Analysis using KL Divergence

For Each Pipeline Output

$$
D_{\text{KL}}(P_{\text{true}} || P_{\text{pipeline}}) = \sum_{x \in X} P_{\text{true}}(x) \log \frac{P_{\text{true}}(x)}{P_{\text{pipeline}}(x)}
$$

Where:

- $P_{\text{true}}(x)$ is the ground truth probability distribution
- $P_{\text{pipeline}}(x)$ is the pipeline output distribution

Accuracy Comparison Ratio

$$
R_{\text{accuracy}} = \frac{D_{\text{KL}}(\text{sequential})}{D_{\text{KL}}(\text{parallel})}
$$

- If $R_{\text{accuracy}} > 1$: Parallel pipeline is more accurate
- If $R_{\text{accuracy}} < 1$: Sequential pipeline is more accurate

##### Resource Utilization Analysis

Memory Efficiency Ratio

$$
E_{\text{memory}} = \frac{M_{\text{sequential}}}{M_{\text{parallel}}}
$$

Where:

- $M_{\text{sequential}}$ is peak memory usage in sequential pipeline
- $M_{\text{parallel}}$ is peak memory usage in parallel pipeline

GPU Utilization Efficiency

$$
E_{\text{GPU}} = \frac{\sum_{t=0}^{T} U_t}{T \cdot N_{\text{GPU}}} \cdot 100%
$$

Where:

- $U_t$ is GPU utilization at time $t$
- $T$ is total execution time
- $N_{\text{GPU}}$ is number of GPUs

##### Real-world Performance Metrics

Throughput

$$
\text{Throughput} = \frac{\text{Number of processed samples}}{\text{Total time}}
$$
Latency Distribution
$$
L_{\text{percentile}}(p) = \text{percentile}({l_1, l_2, ..., l_n}, p)
$$

Where:

- $l_i$ is the latency of sample $i$
- $p$ is the desired percentile (e.g., 95th, 99th)

Comprehensive Performance Score

Combined score considering all metrics:

$$
\text{Score} = w_1\cdot\frac{1}{T} + w_2\cdot\frac{1}{D_{\text{KL}}} + w_3\cdot E_{\text{memory}} + w_4\cdot E_{\text{GPU}}
$$

Where:

- $w_i$ are weights for each metric (Σw_i = 1)
- $T$ is execution time
- $D_{\text{KL}}$ is KL divergence
- $E_{\text{memory}}$ is memory efficiency
- $E_{\text{GPU}}$ is GPU utilization efficiency


##### Key Insights

1. Sequential processing is simple but inefficient for large datasets.  
2. Parallel processing significantly improves processing speed but requires careful optimization, such as load balancing and synchronization.  
3. Kullback–Leibler divergence helps align process data with operational data, ensuring consistency in manufacturing workflows.


##### Another Scenario in vision detection
In manufacturing, pipelines are used to process input data (e.g., RGB images for defect detection). These pipelines can be configured in two ways:
1. **Sequential Pipeline**: Processes tasks one at a time in sequence.
2. **Parallel Pipeline**: Processes multiple tasks simultaneously.

Sequential Pipeline:

$$
D_{\text{KL}}(Q || P_{\text{sequential}}) = 0.8 \cdot \log \frac{0.8}{0.7} + 0.2 \cdot \log \frac{0.2}{0.3}
$$

Result: $D_{\text{KL}}(Q || P_{\text{sequential}}) \approx 0.091$

Parallel Pipeline:

$$
D_{\text{KL}}(Q || P_{\text{parallel}}) = 0.8 \cdot \log \frac{0.8}{0.85} + 0.2 \cdot \log \frac{0.2}{0.15}
$$

Result: $D_{\text{KL}}(Q || P_{\text{parallel}}) \approx 0.061$

Interpretation of Results

Sequential Pipeline: KL Divergence = 0.091
Parallel Pipeline: KL Divergence = 0.061

In this specific example, the parallel pipeline's output (KL Divergence = 0.061) shows better alignment with the reference data compared to the sequential pipeline (KL Divergence = 0.091). However, this should be validated across multiple datasets and considered alongside other performance metrics before making a general conclusion about pipeline superiority.
