import animate
import matplotlib.pyplot as plt
import numpy as np
import palmout
import plot

from topography import Topography

topography_filepath = "C:\\Users\\drowe\\Desktop\\Welcome Daniel\\CIMH - f\\Research\\PALM\\Topography Files\\BRB_DEM_10M_UTM21N.tif"

bds_topo = Topography(
    filepath=topography_filepath
)
bds_topo.make_shape_even()
bds_topo.flip()
bds_topo.mask()
bds_topo.downscale(final_resolution=100)
bds_topo.smooth()

print(
    f"{bds_topo.dataset}"
)


palmout_xy = palmout.PalmOutXY(
    palm_out_filepath="C:\\Users\\drowe\\flow_around_cube_cyclic_xy.000.nc"
)
palmout_xy.normalise()
palmout_xy.update_data_with_normalised_coords()

plot.PlotTopography(bds_topo).plot_xz_cross_section(y=0.7)

