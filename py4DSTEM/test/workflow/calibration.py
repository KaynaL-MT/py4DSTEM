# Calibration workflow

import py4DSTEM
from py4DSTEM.visualize import show
import numpy as np


# Set filepaths
#  - experimental aluminum dataset
#  - a same day/conditions vacuum scan
#  - a path to write to
filepath_calibration_dm = "/media/AuxDriveB/Data/HadasSternlicht/conductive_polymers/500C/dataset_123_aluminumStandard/dataset_123.dm4"
filepath_vacuum = "/media/AuxDriveB/Data/HadasSternlicht/conductive_polymers/500C/dataset_141_vacuumScan/dataset_141.dm4"
filepath_h5 = "/home/ben/Desktop/test.h5"


# Load a datacube from a dm file
datacube = py4DSTEM.io.read(filepath_calibration_dm)
datacube = py4DSTEM.io.datastructure.DataCube(
    data=datacube.data[0:15,0:20,:,:])

print(f"Loaded a {datacube.data.shape} shaped datacube with tree:")
datacube.tree.print()




# Virtual diffraction

dp_max = datacube.get_dp_max()
dp_mean = datacube.get_dp_mean()
dp_median = datacube.get_dp_median()
#show(datacube.tree['dp_max'], scaling='log')
#show(datacube.tree['dp_mean'], scaling='log')
#show(datacube.tree['dp_median'], scaling='log')

print("After virtual diffraction")
datacube.tree.print()





# Virtual imaging

geometry_BF = (
    (432,432),
    30
)
geometry_ADF = (
    (432,432),
    (80,300)
)
im_BF = datacube.get_virtual_image(
    mode = 'circle',
    geometry = geometry_BF,
    name = 'vBF'
)
im_ADF = datacube.get_virtual_image(
    mode = 'annulus',
    geometry = geometry_ADF,
    name = 'vADF'
)
#show(datacube.tree['vBF'])
#show(datacube.tree['vADF'])

print("After virtual imaging")
datacube.tree.print()





# Probe

datacube_vacuum = py4DSTEM.io.read(
    filepath_vacuum,
    name = 'datacube_vacuum'
)
print('Loaded a vacuum datacube:')
print(datacube_vacuum)

probe = datacube_vacuum.get_vacuum_probe(
    ROI = (7,10,7,10)
)

#show(datacube_vacuum.tree['probe'].probe)
#show(datacube_vacuum.tree['probe'].kernel)

probe.get_kernel(
    mode = 'sigmoid',
    radii = (0,50)
)

datacube.add(probe)

print("After probe")
datacube.tree.print()







# disk detection
rxs = 0,3,5,10,5,8
rys = 8,5,13,12,14,3


# Tune disk detection parameters on selected DPs
detect_params = {
    'minAbsoluteIntensity':0.65,
    'minPeakSpacing':20,
    'maxNumPeaks':20,
    'subpixel':'poly',
    'sigma':2,
    'edgeBoundary':20,
    'corrPower':1,
}

selected_peaks = py4DSTEM.process.diskdetection.find_Bragg_disks_selected(
    datacube=datacube,
    probe=probe_kernel,
    Rx=rxs,
    Ry=rys,
    **detect_params
)

#py4DSTEM.visualize.show_image_grid(
#    get_ar=lambda i:datacube.data[rxs[i],rys[i],:,:],
#    H=3,W=2,
#    get_bordercolor=lambda i:colors[i],
#    get_x=lambda i:selected_peaks[i].data['qx'],
#    get_y=lambda i:selected_peaks[i].data['qy'],
#    get_pointcolors=lambda i:colors[i],
#    scaling='power',power=0.125,
#    open_circles=True,
#    scale=200)


# Get all disks
#braggpeaks_raw = py4DSTEM.process.diskdetection.find_Bragg_disks(
#    datacube=datacube,
#    probe=probe_kernel,
#    name='braggpeaks_raw',
#    **detect_params
#)





# BVM

#bvm = py4DSTEM.process.diskdetection.get_bragg_vector_map_raw(braggpeaks_raw,datacube.Q_Nx,datacube.Q_Ny)
















# io

#py4DSTEM.io.save(
#    filepath_h5,
#    datacube,
#    tree = True,
#    mode = 'o'
#)
#py4DSTEM.io.print_h5_tree(filepath_h5)
#
#d = py4DSTEM.io.read(
#    filepath_h5,
#    root = '4DSTEM_experiment/datacube/probe',
#    tree = False
#)
#
#
#print(d)
#print(d.metadata)



