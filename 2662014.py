#Maybe starting to be smarter about making luminosity graphs
#Dean Shaff
import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linalg

import os
import subprocess
import scipy.stats as stats

import astropy.io.fits as fits
from astropy import constants as const

from plotting_tools import Graphs
from plotting_tools import Stats_Stuff
from plotting_tools import Physical_Graphs
#========================================
path_to_gelfand = '/home/dean/gelfand_pwn/2014-06-16'
phot = 'modelres.photspec.fits'
dyn = 'modelres.dyninfo.fits'
#========================================
'''
I can now make graphs in a variety of ranges simply by inputting two lines of code. This may come in handy!
'''
#test = Physical_Graphs()
#test.total_luminosity(lower=2,upper=10,units='keV')

x = np.arange(0,10,0.1)
y = [np.sin(x)]
test2 = Graphs()
fig, ax = test2.basic_plot(x_data=x,y_data=y)
plt.show()
