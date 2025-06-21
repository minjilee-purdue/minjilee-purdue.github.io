### Positional Encoding Visualization: [PE Demo](https://minjilee-purdue.github.io/lecture/transformer/positional-encoding/index.html)

#### An interactive visualization demonstrating how sine and cosine functions transform scalar position values into high-dimensional vectors in Transformer models.

This project illustrates the mathematical process behind positional encoding in Transformer architectures:

- PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
- PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))


Key Concepts Demonstrated:

- Scalar to Vector Transformation: How a single position number becomes a multi-dimensional vector
- Frequency Modulation: Different dimensions use different frequencies to encode position
- Unique Position Signatures: Each position gets a unique vector pattern
- Periodic Patterns: Visual representation of sine/cosine wave behaviors

#### Four Interactive Visualizations
1. Dimension Values Chart

- Shows sine/cosine values for each vector dimension at a specific position
- Interactive controls for position and vector size
- Color-coded positive (red) and negative (blue) values

2. Waveform Analysis

- Displays how each dimension changes across different positions
- Demonstrates the periodic nature of sine/cosine functions
- Shows different frequencies for different dimensions

3. Encoding Heatmap

- Matrix view of all position × dimension combinations
- Visual representation of the complete encoding space
- Each row represents a unique position's encoding vector

4. Frequency Analysis

- Shows the frequency spectrum used by different dimensions
- Logarithmic scale visualization
- Explains why different dimensions capture different temporal patterns

##### Live Demo
GitHub Pages: [Demo is available](https://minjilee-purdue.github.io/lecture/transformer/positional-encoding/index.html)
Inspired by the "Attention Is All You Need" paper
Built with Chart.js for beautiful visualizations
Educational content aimed at making complex concepts accessible

📧 Contact

Minji Lee/lee3450@purdue.edu
