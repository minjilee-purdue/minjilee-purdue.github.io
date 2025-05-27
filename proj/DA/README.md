<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

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
