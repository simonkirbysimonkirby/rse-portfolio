# rse-portfolio

June 2022, Simon Kirby

This repository contains three small pieces of work relating to research I am currently conducting with Prof. Christmas. 
Three apps are included, two in a functional style, and one object-orientated, showing a wide range of techniques, from low-level manipulation 
of geometric primitives, to the creation of engaging visualisations, to optimisation with a genetic algorithm. Please enjoy!

# Dependencies

Dependencies for the project can be found in `requirements.txt`. This was generated using `pipreqs`, so might be too abridged for some users. These can be installed in a virtual environment in the standard way. Most dependencies should be familiar: all visualisations have been created using `matplotlib`, some
arithmetic has been completed with `numpy`, some polygon manipulation with `shapely`, and network creation has been handled with `networkx`.

Two dependencies should be highlighted:
* `descartes`: extends the `matplotlib` patch functionality, which is incredibly useful when plotting room polygons.
  More details can be found [here](https://pypi.org/project/descartes/#description).
* `scikit-geometry`/`skgeom`: this library is used to handle geometric primitives (such as rays, vectors, and planes).
It is a Python wrapper around many of the CGAL types, a mature C++ library. It also contains a number of algorithms to 
  compute straight skeletons, and generally transform primitives in multiple ways. To install, conda users can 
  install via `conda install scikit-geometry -c conda-forge`. Alternatively, installation via the git repository 
  [here](https://github.com/scikit-geometry/scikit-geometry) can be performed. Please see 
  [here](https://wolfv.medium.com/introducing-scikit-geometry-ae1dccaad5fd) for more
  installation instructions.

# General Structure

Each of the two apps has a single entry point with the premix `run_`. Once dependencies have been installed, please 
run this file in your IDE to run the app.

## App 1: Building Layouts

### Introduction

This app creates a traversable network representation from a simple set of room polygons and doorway coordinates. 

The following routine is performed:
* Loads input data
* Plots building layout and doorway locations
* Creates straight skeleton representations of each polygon
* Projects ray through each doorway, connecting the skeletons
* Cuts and sorts skeletons into manageable line segments
* Creates complex network representation of building layout
* Simplifies the network using a three stage routine
* Relabels and saves the final graph

### Input & Outputs

**Inputs**:
* `room_polygons.pickle`: a pickled dictionary of polygons, each representing a room in a building.
* ` building_doorways.pickle`: a pickled dictionary of doorway coordinates and metadata, in particular, information 
about which pairs of rooms are connected via which doorways.
  
**Outputs**:

* `output_1`: image of building rooms and doorway locations
* `output_2`: image of straight skeletons produced for each room
* `output_3`: image of cut line segments, and connecting line segments
* `output_4`: image of an untrimmed, complex network representation of the building
* `output_5`: image of a trimmed building network
* `output_6`: image of the final building network, with a 3-stage trim sequence applied
* `output_7`: the final network of the building, pickled

### How to run

Please run the file `run_building_layouts.py`.

## App 2: Building Navigation

### Introduction

The second app shows a shortest path routing algorithm, using edge weights set to the distances between nodes.

The following routine is performed:
* Loads input data
* Selects two random nodes from different rooms
* Finds the shortest path between these nodes (by distance/edge weight)
* Plots the shortest path on a visualisation of the floor plan

### How to run

Please run the file `run_building_navigation.py`. Run this multiple times to generate different routes!

### Input & Outputs

**Inputs**:
* `room_polygons.pickle`: a pickled dictionary of polygons, each representing a room in a building.
* `building_doorways.pickle`: a pickled dictionary of doorway coordinates and metadata, in particular, information 
about which pairs of rooms are connected via which doorways.
  
**Outputs**:

* `output_1`: image of shortest path between two nodes

## App 3: Genetic Algorithm

### Introduction

The third app takes the building graph produced in app 1, and the shortest path routing abilities shown in app 2, and optimises a travelling salesperson problem (i.e. what is the shortest distance a person visitng n rooms can take, visiting each room in a required route once). This app has been written in a class-based style, simplifying the user entry point significantly. 

The following routine is performed:
* A distance matrix between every room and every other room is created, using the shortest path algorithm shown in app 2.
* A route length is specified (i.e. 20 different rooms must be visited).
* A genetic algorithm is initialised using the parameteres given.
* A genetic algorithm is used to find the sequence of rooms visited to minimise the distance travelled overall.
* Ordered crossover (Davis) is used to generate children, and mutation is used to try to avoid local minima.
* The outputs are processed, a figure saved, and some information printed to the console.

### How to run

Please run the file `run_travelling_person_problem.py`. Change the GA inputs to adjust the optimisation.

### Input & Outputs

**Inputs**:
* `final_building_network.pickle`: final network of building, used to create a distance matrix of shortest paths
  
**Outputs**:

* `output_1`: image of the reduction in distance travelled across epochs







  


