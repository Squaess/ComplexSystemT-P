# Comples Systems Theory and Practice

This is a Repository for storing files for my University Course.

## Setting up the environment

If you would like to reuse and play with
this project, here are the steps to correctly
setup new environment.

1. Make sure that you're using ``python3`` in a ``64`` bit version.
1. Fork this repository and/or clone it:
`git clone https://github.com/Squaess/ComplexSystemT-P.git`
1. Create new virtual environment: `python -m venv venv`
1. Activate the environment:
    * On Windows: `.\venv\Scripts\activate`
    * On Linux/Mac: `source ./venv/bin/activate`
1. Install packages from ``requirements.txt`` file:
`pip install -r requirements.txt`
1. To enable savin files with plotly pleas see this page: [plotly](https://plot.ly/python/static-image-export/). You need to install ``orca``.

## Problem sheet 1

Generated graphs (the png conversion look ugly, better to use plotly and browser):

Dolphin connections:
![doplhins][dolphins]

Collaboration graphs:
![cs_graph][cs_graph]
![phy_graph][phy_graph]
![kft_graph][kft_graph]

[dolphins]: problem_sheet1/results/exc1.png "Connections between dolphins"
[cs_graph]: problem_sheet1/results/graph_cs.png "Graph collaboration."
[phy_graph]: problem_sheet1/results/graph_phy.png "Graph collaboration."
[kft_graph]: problem_sheet1/results/graph_kft.png "Graph collaboration."
