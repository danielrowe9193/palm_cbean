Collection of scripts responsible for the post processing of PALM outputs done in the Caribbean.

# Running A Toy Model In PALM

## Introduction
The primary objective of this tutorial is to introduce the workflow involved in running a PALM simulation, from creating the required directories and input files to visualizing and analyzing the results. The secondary objective is to familiarize users with basic Linux commands, the Python programming language, and the physical principles governing fluid flow around obstacles such as buildings and terrain. 

We will design an experiment called `toy_model`, which will serve as the guide for future experiments the user wishes to run. This tutorial assumes you are on `kratos-head` but it can be translated to other machines.

## Creating Working Directories
The first step is to create the directories that your PALM simulation will use. Navigate to the `JOBS/` directory in PALM
```
cd palm/current_version/JOBS/
```
Create the directory for our experiment `toy_model` 
```
mkdir toy_model
```
Enter the `toy_model/` directory
```
cd toy_model
```
Then create the `INPUT/` directory
```
mkdir INPUT
```
Run the command `pwd` while in the `INPUT/` directory. You should see the following output:
```
/home/kratos-head/palm/current_version/JOBS/toy_model/INPUT
```
which means all directories have been created as required.

## Creating Topography Files
