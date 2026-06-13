Collection of scripts responsible for the post processing of PALM outputs done in the Caribbean.

# Running A Toy Model In PALM

## Introduction
The primary objective of this tutorial is to introduce the workflow involved in running a PALM simulation, from creating the required directories and input files to visualizing and analyzing the results. The secondary objective is to familiarize users with basic Linux commands, the Python programming language, and the physical principles governing fluid flow around obstacles such as buildings and terrain. 

We will design an experiment called `toy_model`, which will serve as the guide for future experiments the user wishes to run. This tutorial assumes you are on `kratos-head` but it can be translated to other machines.

## Creating Working Directories
The first step is to create the directories that your PALM simulation will use. Navigate to the `JOBS/` directory in PALM
```bash
cd palm/current_version/JOBS/
```
Create the directory for our experiment `toy_model` 
```bash
mkdir toy_model
```
Enter the `toy_model/` directory
```bash
cd toy_model
```
Then create the `INPUT/` directory
```bash
mkdir INPUT
```
Run the command `pwd` while in the `INPUT/` directory. You should see the following output:
```bash
/home/kratos-head/palm/current_version/JOBS/toy_model/INPUT
```
which means all directories have been created as required.

## Creating Topography Files
Our experiment `toy_model` investigates the flow of wind around some buildings. To this end, we must create a topography file that contains the buildings and ingest this into PALM. Navigate to `intern_python`
```bash
cd PythonRelated/intern_python
```
Next, we must activate the Python virtual environment (venv). Virtual environments act as isolated workspaces for Python projects, allowing packages to be installed and managed separately from the system's default Python installation. This helps keep projects organized and avoids conflicts between package versions. Activate the venv using
```bash
source intern/bin/activate
```
You should see something like `(intern) kratos-head@kratos-head`, which means the venv is activated. I have created a python file `toy_topography.py` that allows you to add buildings and create the topography file. Edit `toy_topography.py` by either going to into the `scripts/` directory first
```bash
cd scripts/
vi toy_topography.py
```
or accessing the file while staying in the `intern_python/` directory.
```bash
vi scripts/toy_topography.py
```
At the end of `toy_topography.py` you will see
```python
# example usage
# feel free to change the parameters around!
# maybe you want a larger domain or more buildings!

toy_topo = ToyTopography(size_of_domain=(100, 100))
toy_topo.add_building(x_span=(20, 40), y_span=(20, 80), height=40)
toy_topo.save_topofile("/path/to/your/directory", "name_of_file")
```
Once you have finished editing the topography file, save, exit and run the script using
```bash
python toy_topography.py
```
