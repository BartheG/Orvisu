# Orvisu

Orvisu provides an interface to simply generate 3D plot and 3D animations with color as 4th dimensions.

Orvisu is a Python3 interface realized with [wxpython](https://wxpython.org/)

Orvisu uses [PVGeo](https://github.com/OpenGeoVis/PVGeo) and [pyvista](https://github.com/pyvista/pyvista) libraries for the visualization.

Orvisu can be useful in Geoscience to visualize 3D Domains or visualize sliced 3D domain.

## UBC file format

Orvisu uses UBC file format to generate plots. For one plot two files are needed:

- [mesh](https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh3Dfile.html)
- [model](https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/modelfile.html)

The mesh defines the model region and the model file defines the cells properties.

A script named "writeVisuOutput.py" is provided to generate UBC files from [numpy](https://www.numpy.org/) arrays.

Example:

```python
import sys
sys.path.append('/path/to/Orvisu/directory')
import writeVisuOutput as wvo
import numpy as np

data=np.random.rand(3,3,3)
wvo.WriteVisuOutput().run(data,'ubc','./numpytoubc')

s_data=np.ones((5,10,15))*10
wvo.WriteVisuOutput().run(s_data,'ubc','./s_numpytoubc')
```

## Requirements

- [Python3.x](https://www.python.org/downloads/) needs to be installed.
- Package manager [pip](https://pip.pypa.io/en/stable/) needs to be installed.

## Installation

Use the 'install.sh' script.
```bash
git clone https://github.com/BartheG/Orvisu.git
chmod +x ./install.sh && ./install.sh
``` or ```bash
git clone https://github.com/BartheG/Orvisu.git
chmod +x ./install.sh && sudo ./install.sh
```

## Usage

```bash
python3 CoreInterface.py
```

![Usage example](https://github.com/BartheG/Orvisu_pres/blob/master/DemoUsage.gif?raw=true)

## Examples of visualizations made with Orvisu

![Plot showing a 50\*50 (horizontal blocks) domain with PH value as 4th dimension](https://github.com/BartheG/Orvisu_pres/blob/master/demoplot.png?raw=true)
![Animation showing the evolution of a 15\*15 (horizontal blocks) domain with PH value as 4th dimension](https://github.com/BartheG/Orvisu_pres/blob/master/demoreadme.gif?raw=true)
![Animation showing the evolution of a 50\*50 (horizontal blocks) domain with PH value as 4th dimension](https://github.com/BartheG/Orvisu_pres/blob/master/demofulldomain.gif?raw=true)

## Contact
[Guillaume Barthe](https://fr.linkedin.com/in/guillaume-barthe-174a22174)
