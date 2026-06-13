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

## Editing Namelist File
Now, we must edit the namelist file that tells PALM what to do. But first we need to get that namelist file into the `INPUT` directory since it doesn't exist currently. The easiest way to do that is to copy the namelist file from another experiment into ours. First navigate to the `JOBS/` directory
```bash
cd palm/current_version/JOBS/
```
Then we copy the namelist file from `flow_around_cube_cyclic` to `toy_model/INPUT/` using the command `cp`:
```bash
cp flow_around_cube_cyclic/INPUT/flow_around_cube_cyclic_p3d toy_model/INPUT/
```
Now we can enter the `INPUT/` directory of our `toy_model`.
```bash
cd toy_model/INPUT/
```
And rename the namelist file to match our experiment using the `mv` command
```bash
mv flow_around_cube_cyclic_p3d toy_model_p3d
```
Proceed to edit `toy_model_p3d` by using
```bash
vi toy_model_p3d
```
There are many variables that must be changed in order for PALM to run successfully. Below, I mention the variables you should change for this tutorial. First, define the `nx`, `ny` and `nz` parameters:
```
    nx                         = 199, ! Number of gridboxes in x-direction (nx+1)
    ny                         = 199, ! Number of gridboxes in y-direction (ny+1)
    nz                         = 50, ! Number of gridboxes in z-direction (nz)
```
You will get `nx` and `ny` depending on the size of your domain that you set when creating the topography. Recall that PALM requires `nx` and `ny` to be 1 value less than your code. If the size of your domain in the x direction is `200`, then `nx=199` and similarly for `ny`. You should set `nz` to a value that is some distance higher than the tallest building in your domain so your simulation captures the full dynamics. For example, if the height of the tallest building in your domain is $40$ gridpoints, then its wise for `nz` to be $60$ or greater. 

Then we define the size of our grid
```
	dx                         = 2.0, ! Size of single gridbox in x-direction
	dy                         = 2.0, ! Size of single gridbox in y-direction
	dz                         = 2.0, ! Size of single gridbox in z-direction
```
where the unit here is meters. 

Of course, nothing interesting can happen if we don't initialize the $u$ and $v$ components of our flow:

```
	ug_surface                 = 0.0, ! initial u-comp
	vg_surface                 = 0.0, ! initial v-comp
```

where of course you can set the wind flow to be whatever you like. Another defining aspect of our flow is the pressure gradient:

```
	dp_external                = .F.,          ! use horizontal pressure gradient
	dpdxy                      = -0.0002, 0.0, ! set pressure gradient along x
```

where for our `toy_model` we set `dp_external` to false. `end_time` determines the simulation length, in seconds:

```
	end_time                   = 1800.0, ! simulation time of the 3D model
```

The compute time of your simulation increases the larger the `end_time` is.  

```
	dt_data_output             = 1.0, ! output interval for general data
```

Let the temporal resolution of our output data be 1 second, so we can truly capture the flow evolution. 

```
    section_xy                 = 1, 10, 30,
    section_xz                 = 40, 100, 150,
    section_yz                 = 2, 40

    data_output                = 'wspeed_xy', 'wdir_xy', 'wspeed_xz', 'wdir_xz', 'wspeed_yz', 'wdir_yz'
```

`section_xy` allows us to select the `z` indices at which we want a cross section to be taken. Similarly, `section_xz` allows us to select the `x` indices at which we want a vertical cross section to be taken. `section_yz` follows the same logic. Here, we consider the wind speed and direction in each of the planes we have defined only. All the variables not mentioned here should be left unchanged, and you can find a description of all parameters at [here](https://palm.muk.uni-hannover.de/trac/wiki/doc/app/initialization_parameters). With the namelist file ready, we can then run PALM.

## Running PALM
To run PALM is quite simple. Use this command in any directory:
```bash
/home/kratos-head/palm/current_version/bin/palmrun -r toy_model -c default -a "d3#" -X 4 -v -z &> /home/kratos-head/palm/logs/log.toy_model_exp1 &
```
To make sure that PALM is running, use
```bash
top
```
to get a view of of current processes on `kratos-head`. If PALM is running, you should see 4 processes running on each of the cores, dedicated to PALM. You can track the progress of the run by using
```bash
vi palm/logs/log.toy_model_exp1
```

## Accessing Results
Once PALM is completed, it will create a directory called `OUTPUT/` in the experiment directory:
```bash
/home/kratos-head/palm/current_version/JOBS/toy_model/OUTPUT/
```
In this directory will be all the `.nc` files that are created.

## Visualization Using Python
