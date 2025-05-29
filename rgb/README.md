# RGB Color Vector Visualization

An interactive 3D visualization that demonstrates how RGB colors can be represented as vectors in 3-dimensional space.

## 🚀 Live Demo

**[View Interactive Demo](https://minjilee-purdue.github.io/rgb/index.html)**

## 📊 What This Shows

This visualization helps understand the mathematical relationship between colors and vectors by:

- Representing each RGB color as a 3D vector `(R, G, B)`
- Showing the color space as a cube where each axis represents one color channel
- Displaying real-time vector magnitude and coordinates
- Demonstrating how colors relate to geometric positions in 3D space

## 🎮 Features

- **Interactive 3D View**: Mouse drag to rotate and explore the color space
- **Real-time Controls**: RGB sliders to adjust color values dynamically  
- **Vector Mathematics**: Live calculation of vector magnitude and coordinates
- **Preset Colors**: Quick access to primary colors and common combinations
- **Educational Info**: Mathematical explanations of color-vector relationships

## 🧮 Mathematical Concepts

### Vector Representation
- **Origin (0,0,0)**: Black color - no light
- **Unit Vectors**: 
  - Red: (255,0,0)
  - Green: (0,255,0) 
  - Blue: (0,0,255)
- **Vector Magnitude**: `√(R² + G² + B²)`
- **Maximum Distance**: 441.67 (from black to white)

### Color Space
- **Dimensions**: 256 × 256 × 256 cube
- **Total Colors**: 16,777,216 possible combinations
- **Coordinate System**: Cartesian with RGB axes

## 🛠️ Technical Details

- **Built with**: Three.js for 3D rendering
- **Responsive Design**: Works on desktop and mobile
- **Browser Support**: Modern browsers with WebGL support
- **No Dependencies**: Self-contained HTML file

## 📱 Usage

1. **Adjust Colors**: Use the RGB sliders to change color values
2. **Rotate View**: Click and drag to rotate the 3D scene
3. **Try Presets**: Click color buttons for common colors
4. **Observe Vectors**: Watch how the white line (vector) changes with different colors

## 🎯 Educational Applications

Perfect for:
- **Computer Graphics Courses**: Understanding color spaces
- **Linear Algebra**: Vector concepts and 3D coordinate systems
- **Digital Art**: Color theory and RGB relationships
- **Programming**: Visual representation of data structures

## 📋 Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/rgb-vector-visualization.git
   ```

2. Open `index.html` in your browser, or

3. Enable GitHub Pages in repository settings to host online

## 🤝 Contributing

Feel free to:
- Report bugs or suggest features
- Submit pull requests for improvements
- Use this in educational materials
- Fork for your own projects

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Related Resources

- [Three.js Documentation](https://threejs.org/docs/)
- [RGB Color Model - Wikipedia](https://en.wikipedia.org/wiki/RGB_color_model)
- [Linear Algebra and Vectors](https://en.wikipedia.org/wiki/Vector_space)

---

**Made with ❤️ for education and exploration of mathematical concepts in computer graphics.**
