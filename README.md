# Dataset_step
Generate .ply dataset from step files (.stp)

# Dataset Generation from STEP Files

This script converts STEP files into STL format and generates point cloud datasets in PLY format using Python with Open3D and Trimesh libraries.

## Requirements

- Python 3.x
- Required Python packages:
  - `open3d`
  - `trimesh`

Install dependencies using `pip`:
```bash
pip install open3d trimesh
```

# Usage

`convert_to_stl(input_folder, output_folder)`

Converts STEP files in the input folder to STL format and saves them in the output folder.

Parameters:

- input_folder (str): Path to the folder containing the STEP files.

- output_folder (str): Path to the folder where the converted STL files will be saved.

```python
from pathlib import Path
import trimesh

def convert_to_stl(input_folder: str, output_folder: str):
```

generate_ply_folders(input_folder, output_folder, number_of_points)

Generates PLY folders by converting STEP files to STL and sampling points.

Parameters:

- input_folder (str): Path to the input folder containing STEP files.
- output_folder (str): Path to the output folder where the PLY folders will be generated.
- number_of_points (list): List of integers representing the number of points to sample.

```python
from pathlib import Path
import open3d

def generate_ply_folders(input_folder: str, output_folder: str, number_of_points: list):
```

generate_dataset_from_step(dataset_path, number_of_points=[1000, 5000, 10000])

Generates a dataset from a given STEP file directory.

Parameters:

- dataset_path (str): Path to the dataset containing STEP files.
- number_of_points (list, optional): List of integers representing the number of points to generate for each STEP file. Default is [1000, 5000, 10000].

```python
from pathlib import Path

def generate_dataset_from_step(dataset_path: str, number_of_points: list = [1000, 5000, 10000]):
```

# exemple 

```python
if __name__ == "__main__":
    dataset_path = "data/step_test"
    generate_dataset_from_step(dataset_path, [1000, 5000, 10000])
```

# Data Structure

This script assumes the presence of STEP files in the specified dataset_path. It converts these STEP files into STL format, then generates PLY files with varying point densities as specified in number_of_points.

Before running the code : 
```
dataset
│   STEP_files 
│   │   772805.stp 
│   │   772806.stp 
│   │   ...
│   
```

After running the code : 

```
dataset
│   STEP_files 
│   │   772805.stp 
│   │   772806.stp 
│   │   ...
│   
└─── output
    │
    └───1000
    │    │   772805.ply
    │    │   772806.ply
    │    │   ...
    │
    └───5000
    │    │   772805.ply
    │    │   772806.ply
    │    │   ...
    │
    └───10000
    │    │   772805.ply
    │    │   772806.ply
    │    │   ...

```