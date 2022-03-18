![logo_wide](https://user-images.githubusercontent.com/23581140/158681822-8e8d7d4c-c7d2-4ce0-a5e8-23d2a9a500a8.png)
# Tactile-Sensing-Development-Framework

A visual tool for fast fabrication of tactile sensors

## How to use

### Unwrapping Objects
Currently the only supported extension is .obj. Furthermore the following restrictions are given:
- Geometry must be manifold
- Exacly one connected figure inside the file
- Mesh has to be triangulation
- The file must not be binary
- No unused vertices are allowed

### Patterns
Once the flat surfaces are visible, patterns can be placed onto them. These are available in a list which also contains visualizations for each pattern's parameters. All length units are measured in millimeters.

## Building from source
Libraries used are [Numpy](https://numpy.org/), [Libigl](https://libigl.github.io/libigl-python-bindings/), [OpenMesh](https://www.graphics.rwth-aachen.de/software/openmesh/), [Matplotlib](https://matplotlib.org/), [Plotly](https://plotly.com/), [Pillow](https://pypi.org/project/Pillow/) and [Rectpack](https://github.com/secnot/rectpack). The program can be run by executing main.py; for generation of windows executables pyinstaller.py can be used, requiring the [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/usage.html) library.

## Contributing
The application's modularity allows for easy integration of additional algorithms and distortions but especially new patterns
### Algorithms
### Patterns

### Possible Future Work
- Folder system for patterns inside the application to provide a clear overview and fast accessibility of all patterns
- Enable manual chart merging for a more user-controlled segmentation
- Storing the application state enabling undo and redo operations

---
Created by Nicolai Stein in 2022 as part of a Bachelor's Thesis. This application is intended for research purposes. Contact: nicolai_stein@outlook.de
