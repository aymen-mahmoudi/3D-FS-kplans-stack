# 3D FS or kplans stack



## Description

Comparing the isoenergy cuts of an FS ARPES data can be very helpful in checking the homogeneity of domains and tracking the BZ shape evolution against the binding energy. This script enables a 3D superposition of isoenergy cuts.
<br>
<br>   
This program was used to generate the output example above published in https://pubs.acs.org/doi/abs/10.1021/acsnano.3c04186

<img src="./resources/3D_output_sample.png"
     alt="3D output sample"
      style="float: center"/>

Aside from the tracking of the BZ shape evolution, the evolution of bands against the k position cut can be useful as illustrated in the example below: 
<img src="./resources/3D_output_sample.png"
     alt="3D output sample"
      style="float: center"/>
## Installation
You need just jupyter notebook editor with a recent version of a Python interpreter (the easiest way to get both will be via anaconda distribution : https://www.anaconda.com/). The use of the jupyter notebook is super friendly, you have just to offord the suitable libraries. If you want to use it via a venv, It is already tested under python 3.8 (just make sure you install the librairies in the file requirements.txt). To generate the 3D stack, you need only to tune the parameteres to have the output you want.
<br>
For the moment, only the notebook version is available. I plan to create a Qt app version of it soon (laziness problem). 

## Usage
First, you have to prepare the isoenergy cuts and name them under the following format **EnergyValueeV.extension** (-0.7eV.jpg, -1.27eV.png). All extension of 3 or 4 letters are accepted (png, jpg, jpeg, etc). Then, you need to add the folder path where your figures are located.
<br>
Once, the figures are ready, the kx and ky ranges have to be added to reshape the figures. Then the final cell enable to generate the stacking, and it offers a bunch of settings to customize your final figures.
<br>
<em>If you don't have any data yet. You can use the isoenergy cuts provided in the folder: "resources/FS_samples" to run the script</em>
<br>
If you are confortable enough with the program, you can use the extended version which has extra cells to offer additional preprocessing of the input images (scaling and rotating) before processing the stack.
<be>
N.B: This project can be used to generate a 3D stack for any other type of graph.


## Support and Contributing
In case of problem, It is strongly recommended to post an issue. For a more confidential demand, you can email to mahmoudi7050@gmail.com
<br>
Don't hesitate if you have any suggestions/ideas to enhance those scripts or to add further settings. Your suggestion are warmly welcomed.
