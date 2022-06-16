# rse-portfolio

June 2022, Simon Kirby

This repository contains two small pieces of work relating to research I am currently conducting with Prof. Christmas. 
Two small apps are included, both in a functional style, showing a wide range of techniques, from low-level manipulation 
of geometric primitives, to the creation of engaging visualisations. Please enjoy!

# Dependencies

Dependencies for the project can be found in `requirements.txt`. These can be installed in a virtual environment in 
the standard way. Most dependencies should be familiar: all visualisations have been created using `matplotlib`, some
arithmetic has been completed with `numpy`, and network creation has been handled with `networkx`.

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

# App 2: Building Navigation

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
* ` building_doorways.pickle`: a pickled dictionary of doorway coordinates and metadata, in particular, information 
about which pairs of rooms are connected via which doorways.
  
**Outputs**:

* `output_1`: image of shortest path between two nodes







  


