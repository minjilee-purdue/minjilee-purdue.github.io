<table>
<tr>
<td width="40%">
  <img src="/proj/DA/orig_mask.png" alt="Pipeline Overview" style="max-width:100%;">
</td>
<td style="vertical-align: top; padding-left: 20px;">

# Data Acquisition and Semantic Reasoning Pipeline

This section describes an end-to-end pipeline for semantic segmentation of Eastern Red Cedar trees using UAV imagery. It integrates data acquisition, processing, and reasoning modules designed to support ecological monitoring and management.

</td>
</tr>
</table>

## III. IMPLEMENTATION

### [Data Acquisition](proj/DA/README.md)  
**Multimodal Semantic Segmentation of Eastern Red Cedar Trees: Integrating Visual Masks and Natural Language Prompts**

### A. Data Collection

Aerial imagery was collected using an **Autel Robotics XT705 UAV** equipped with a **1/2.3-inch CMOS sensor**. The native image resolution is **5472 × 3648 pixels**, which can be evenly divided into a **3×3 grid**, yielding nine segments of **1824 × 1216 pixels** each. The UAV maintained a flight height of approximately **30 meters AGL (Above Ground Level)**.

Environmental factors (e.g., wind, barometric variation, and GPS drift) introduced a vertical deviation of **±1 meter**, reflecting typical field conditions without RTK correction.

---

### B. Image Processing Methodology

To calculate the real-world size of segmented regions, we used the **Ground Sampling Distance (GSD)**, derived from:

$$
\text{GSD (m/pixel)} = \frac{S_w \cdot H}{f \cdot I_w}
$$

Where:

- `S_w` = Sensor width (m)
- `H` = Flight altitude AGL (m)
- `f` = Focal length (m)
- `I_w` = Image width (pixels)

Then:

$$
\text{Pixel Area (m²)} = \text{GSD}^2
$$

$$
\text{Object Area (m²)} = N \cdot \text{GSD}^2
$$

#### Example Calculation

- $S_w = 0.0063$ m  
- $f = 0.013$ m  
- $I_w = 5472$ px  
- $H = 30$ m  
- $N = 1,116,819$ (white mask pixels)

Step 1:

$$
\text{GSD} = \frac{0.0063 \cdot 30}{0.013 \cdot 5472} \approx 0.002656 ~\text{m/pixel}
$$

Step 2:

$$
\text{Pixel Area} = (0.002656)^2 \approx 0.00000705 ~\text{m²}
$$

Step 3:

$$
\text{Estimated Canopy Area} = 1,116,819 \cdot 0.00000705 \approx 7.88 ~\text{m²}
$$

Variation due to altitude:

- At $H = 29$ m:

$$
\text{GSD} \approx 0.002566 \Rightarrow \text{Area} \approx 7.35 ~\text{m²}
$$

- At $H = 31$ m:

$$
\text{GSD} \approx 0.002746 \Rightarrow \text{Area} \approx 8.44 ~\text{m²}
$$

---

### C. From Instance-Level Annotation to Semantic Reasoning

Each segmented tree instance is stored as a JSON object:

```json
{
  "filename": "image_001.png",
  "objects": [
    {
      "class": "eastern_red_cedar",
      "size": "medium",
      "location": "upper-right",
      "bbox": [3311, 241, 4478, 1198]
    },
    {
      "class": "eastern_red_cedar",
      "size": "small",
      "location": "upper-right",
      "bbox": [3298, 0, 4454, 478]
    },
    {
      "class": "eastern_red_cedar",
      "size": "small",
      "location": "lower-right",
      "bbox": [4559, 3192, 4778, 3374]
    }
  ]
}
```

These annotations allow the generation of prompts for LLMs (e.g., GPT-4), enabling automated scene understanding and ecological decision support.

> Example Prompt:  
> “Two small ERC trees are located in the lower-right quadrant near one large tree. This configuration suggests a seed dispersal cluster.”

---

## IV. RESULTS AND DISCUSSION

A total of **194 images** and corresponding **segmentation masks** were analyzed, with each image containing on average **four Eastern Red Cedar (ERC) trees**. About **20 outlier instances** were identified.

Each image generated one structured **JSON file** containing per-instance:

- Class  
- Size  
- Grid location  
- Bounding box  

These annotations were used for:

- Scene-level reasoning  
- LLM prompt generation  
- Ecological summary generation  

---

### A. From Perception to Reasoning

The system integrates vision + spatial data with a language model for:

- Identifying early-stage vs. established ERC clusters  
- Estimating removal complexity  
- Generating actionable insights for land managers  

---

### B. Key Outcomes

- Real-world canopy size estimations  
- Location classification via 3×3 grid  
- JSON-based semantic annotation  
- Scene summarization using language prompts  

This bridges perception and reasoning, enabling intelligent land management.

---

### C. Limitations

- Assumes consistent 3×3 spatial grid  
- Designed specifically for ERC detection  
- Sensitive to UAV altitude deviations  
- Reasoning remains rule-based and not adaptive
