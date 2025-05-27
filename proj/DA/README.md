To calculate the real-world size of segmented regions, we used the **Ground Sampling Distance (GSD)**, derived from:

$$\text{GSD (m/pixel)} = \frac{S_w \cdot H}{f \cdot I_w}$$

Where:
- $S_w$ = Sensor width (m)
- $H$ = Flight altitude AGL (m)  
- $f$ = Focal length (m)
- $I_w$ = Image width (pixels)

Then:
$$\text{Pixel Area (m²)} = \text{GSD}^2$$
$$\text{Object Area (m²)} = N \cdot \text{GSD}^2$$
