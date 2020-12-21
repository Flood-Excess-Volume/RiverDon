# RiverDon

![doncatchment](figs/sheffield_catchment.jpg)

## FEV Matlab analysis for the summer 2007 flood of the River Don in Sheffield

Work published on the (Earth)Arxiv as: 

Bokhove, O., Kelmanson, M., & Kent, T. (2018): On using flood-excess volume to assess natural flood management, exemplified for extreme 2007 and 2015 floods in Yorkshire. *EarthArxiv*. [DOI](https://doi.org/10.31223/osf.io/87z6w).

*Above figure (source: University of Sheffield https://www.sheffield.ac.uk/doncatchment/about (c) Crown Copyright/database right 2011; an Ordnance Survey/EDINA supplied service; river layer kindly licensed from the Environment Agency): The River Don around the Sheffield City region, including the upper Don catchment and the River Sheaf. In Sheffield, the Don is fed by four other rivers: the Sheaf, Loxley, Riverlin, and Porter. The Sheffield Hadfields gauge is located centrally downstream of the Sheaf.*


### Some Graphical output 

#### Data analysis: from depth to discharge to FEV

From the ```/code``` dir, run: 
 * ```quadrantplot_sheff.m```
 
This carries out the FEV calculations and calls four plotting routines at the end of the sript:
 * ```plot3panelerr;```
 * ```plotFEVhT;```
 * ```plot_h_year;```
 * ```plot_ratingcurve;```
 
<img src="figs/shef_3panel_err.png" width="480">


#### Cost-effectiveness analysis: seasonal rainfall scenarios

From the ```/code``` dir, run ```donfloodallev_auto_new.m```. Choose the season alternately:
```
nws = 1; % summer
% nws = 0; % winter
```

![don summer](figs/donallev_summer.png) | ![don winter](figs/donallev_winter.png) 
:-------------------------:|:-------------------------:

*Caption (adapted from fig. 9 in Bokhove, Kelmanson, Kent (2018)): A graphical overview of the fraction of the FEV captured by the two flood-storage measures, reservoirs and leaky dams in the reservoir and Upper Don areas of the Don catchment, respectively, for (a) the summer-rainfall scenarios and (b) the winter-rainfall scenarios. Stacked vertically are the respective probability distributions, relative to the associated FEV, which is fixed for all scenarios. The blue shaded areas to the left of the thick, stepped, solid line denote the fractions of the FEV mitigated per scenario, to be read horizontally (e.g., 93.3% for (S3a)). The mean FEV (winter 44.08%, summer 43.25%) over all 7 scenarios and standard deviation (winter 17.51%, summer 16.38%) are indicated by thick and thin vertical dashed lines respectively.*

## FEV Python analysis for 2007 and 2019 flood of the River Don in Sheffield and Doncaster

Contributors: Zheming Zhang with Onno Bokhove

## FEV analysis using Python/Excel for 2007 and 2019 floods of River Don(Rotherham and Sheffield)

This work was first published in a report for the Data Science project at the University of Leeds.

The River Don is an English river mainly in South Yorkshire and the East Riding of Yorkshir. It source lies in the Pennines and the river flows eastwardly through major British cities such as Sheffield, Rotherham and Doncaste, and eventually merges into the River Ouse. The total length of River Don is 70 miles (110km) and around 1.3 million people are living along the river.

### Graphical output

From the ```/code``` directiry, run:
* ```Integratedcode``` FEVRiverDon.py (by setting the bespoke input file, i.e. TBC)

Eight figures are produced:

![Figures](/Figures/hadfields%202007.png) | ![Figures](/Figures/hadfields%202019.png)
:-------------------------:|:-------------------------:

![Figures](/Figures/tesco%202007.png) | ![Figures](/Figures/tesco%202019%20.png)
:-------------------------:|:-------------------------:

* Caption: Top left and right are the integrated hydrographs of River Don in Sheffield 2007 and 2019 flood events, respectively. Bottom left and right are integrated hydrographs of River Don in Rotherham 2007 and 2019 flood events, respectively. *

#### Cost-effectiveness analysis

![Figures](/Figures/2007%20scheme.png) | ![Figures](/Figures/2019%20shceme.png)
:-------------------------:|:-------------------------:

<img src="/Figures/sheffield%20schemes.png" width="480">
:-------------------------:

* Caption: Figures 1 and 2 are hypothetical schemes for Rotherham in both 2007 and 2019 River Don flood events, Figure 3 reveals the flood mitigation schemes provided by Sheffield City Council; all of these three schemes could alleviate 100% of flood water. *




