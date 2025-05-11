# Referential Vectors

A Python tool for coordinate system conversions and vector calculations in physics and mathematics.

## Features

### Coordinate System Conversions
- Convert between Cartesian, Cylindrical, and Spherical coordinate systems
- Support for both forward and backward conversions
- Automatic coordinate system validation

### Vector Calculations
- Calculate dot products using both Cartesian and trigonometric methods
- Calculate cross product magnitudes using both Cartesian and trigonometric methods
- Support for both vector components and magnitudes with angles

## Usage

### Coordinate System Conversion
```python
from referential_vectors import CoordinateConverter

# Example: Convert from Cartesian to Cylindrical
converter = CoordinateConverter(x=1, y=1, z=1)
print("Cylindrical:", converter.convert('cartesian', 'cylindrical'))

# Example: Convert from Cylindrical to Spherical
converter = CoordinateConverter(rho=1, phi=0.785, z=1)
print("Spherical:", converter.convert('cylindrical', 'spherical'))

# Example: Convert from Spherical to Cartesian
converter = CoordinateConverter(r=2, theta=0.785, phi=0.785)
print("Cartesian:", converter.convert('spherical', 'cartesian'))
```

### Vector Calculations
```python
from referential_vectors import Vects

# Example: Calculate dot and cross products using vector components
vector = Vects(x1=1, y1=2, z1=3, x2=4, y2=5, z2=6)
dot, cross = vector.convert(Trig=False)
print(f"Dot product: {dot}, Cross product magnitude: {cross}")

# Example: Calculate dot and cross products using magnitudes and angle
vector = Vects(md1=3, md2=4, ang=0.785)
dot, cross = vector.convert(Trig=True)
print(f"Dot product: {dot}, Cross product magnitude: {cross}")
```

## Requirements
- Python 3.x
- NumPy

## Installation
```bash
pip install numpy
```

## Note
This tool is designed for educational and research purposes in physics and mathematics, particularly for coordinate system conversions and vector calculations.
