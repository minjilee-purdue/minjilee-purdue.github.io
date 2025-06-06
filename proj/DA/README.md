**A. Data Collection**

Aerial imagery was collected using an **Autel Robotics XT705 UAV** equipped with a **1/2.3-inch CMOS sensor**. The native image resolution is **5472 × 3648 pixels**, which can be evenly divided into a **3×3 grid**, yielding nine segments of **1824 × 1216 pixels** each. The UAV maintained a flight height of approximately **30 meters AGL (Above Ground Level)**.

Environmental factors (e.g., wind, barometric variation, and GPS drift) introduced a vertical deviation of **±1 meter**, reflecting typical field conditions without RTK correction.

---

**B. Image Processing Methodology**

To calculate the real-world size of segmented regions, we used the **Ground Sampling Distance (GSD)**, derived from:

\\[\text{GSD (m/pixel)} = \frac{S_w \cdot H}{f \cdot I_w}\\]

Where:
* \\(S_w\\) = Sensor width (m)
* \\(H\\) = Flight altitude AGL (m)
* \\(f\\) = Focal length (m)
* \\(I_w\\) = Image width (pixels)

Then:

<p><strong>GSD (m/pixel) = (S<sub>w</sub> × H) / (f × I<sub>w</sub>)</strong></p>

---

**Example Calculation**

* \\(S_w = 0.0063\\) m
* \\(f = 0.013\\) m
* \\(I_w = 5472\\) px
* \\(H = 30\\) m
* \\(N = 1,116,819\\) (white mask pixels)

**Step 1:**

\\[\text{GSD} = \frac{0.0063 \cdot 30}{0.013 \cdot 5472} \approx 0.002656 \text{ m/pixel}\\]

**Step 2:**

\\[\text{Pixel Area} = (0.002656)^2 \approx 0.00000705 \text{ m²}\\]

**Step 3:**

\\[\text{Estimated Canopy Area} = 1,116,819 \cdot 0.00000705 \approx 7.88 \text{ m²}\\]

**Variation due to altitude:**

* At \\(H = 29\\) m:
  
  \\[\text{GSD} \approx 0.002566 \Rightarrow \text{Area} \approx 7.35 \text{ m²}\\]

* At \\(H = 31\\) m:
  
  \\[\text{GSD} \approx 0.002746 \Rightarrow \text{Area} \approx 8.44 \text{ m²}\\]

---

**C. From Instance-Level Annotation to Semantic Reasoning**

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
