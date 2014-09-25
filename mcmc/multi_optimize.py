#multiprocessing optimization 
"""
This program uses Python's multiprocessing module to run the optimizaton routine 4 times simultaneously. 
It uses 4 different starting parameters, and then dumps the text file containing the log and the .fits files in the directory specified in each run. 

"""
from multiprocessing import Process
from pwnmodel_mcmc1 import Output
from pwnmodel_mcmc1 import Observables
import numpy as np 
import astropy.io.fits as fits
from astropy import constants as const
import astropy.units as u
from numpy import linalg
import scipy.optimize as op
import emcee
import time
import os
import subprocess
import sys
from optimize import optimize_neglikelihood

mcmc_path = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc'
path_default = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/default_fits'
path1 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing1'
path2 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing2'
path3 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing3'
path4 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing4'

theta1 = [1,8,0.001,3,500,0,0.001,1,1e6,1e3,1.5,2.5]
theta2 = [0.1, 8, 1, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5]
theta3 = [1, 15, 1, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5]
theta4 = [1, 8, 1, 3, 500, 0, 0.0001, 1, 1000000.0, 1000.0, 1.5, 2.5]

if __name__ == '__main__':
	process1 = Process(target=optimize_neglikelihood,args=(theta1,path1))
	process2 = Process(target=optimize_neglikelihood,args=(theta2,path2))
	process3 = Process(target=optimize_neglikelihood,args=(theta3,path3))
	process4 = Process(target=optimize_neglikelihood,args=(theta4,path4))
	process1.start()
	process2.start()
	process3.start()
	process4.start()

