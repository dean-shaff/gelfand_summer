from pwnmodel_mcmc1 import Output
from pwnmodel_mcmc1 import Observables
import numpy as np 
import astropy.io.fits as fits
from astropy import constants as const
import astropy.units as u
from numpy import linalg
import emcee
import time
import os
import subprocess
#========================================
path_to_test = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing'
phot = 'modelres.photspec.fits'
dyn = 'modelres.dyninfo.fits'
elec = 'modelres.elecspec.fits'
#Constants=====================
d = 4.7
char_age = 4850 
edot = 3.3
tstep = -1
#Model Parameters===============
esn = 1 #supernova explosion energy
mej = 8 #ejecta mass
nism = 1 #ISM density 
brakind = 3 #braking index
tau = 500 #spin-down timescale
etag = 0 #(?) fraction of spin-down luminosity lost as radiation #update 16-6-2014 - set this to zero
etab = 0.001 #magnetization of PW
emin =  1 #minimum particle energy 
emax = 10e6 #maximum particle energy 
ebreak = 10e3 #break energy in PW
p1 = 1.5 #below the break
p2 = 2.5 #above the break
#Calculated and random stuff======
age_ = float(((2*char_age)/(brakind-1))-tau)#(?) age of system #says age > 29000 (?) 
e0_ = float(edot*(1+(age_/tau))**((brakind+1)/(brakind-1))) #initial spin-down luminosity (10^37 ergs/s)
velpsr = 0 #update 16-6-2014 - velocity is zero
f_max = 0 #fraction in maxwellian component
kT_max = 0 #energy of maxwellian component
nic = 0 #number of background photon field
ictemp = 0 #temperature of background photon field
icnorm = 0 #normalization of background photon field

runner = Output()
runner.gen_output(tstep,esn,mej,nism,brakind,tau,age_,e0_,velpsr,etag,
	etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic,ictemp,icnorm, directory_path=path_to_test)
os.chdir(path_to_test)
reader = Observables(phot,dyn,elec)
print(reader.photon_density(1,'TeV',d,timing=True)) 
print(reader.grab_flux_density(1.43, 'GHz', d,timing=True))
print(reader.grab_total_flux(0.5,10,'keV',d,timing=True))
print(reader.photon_index(0.5,10,'keV',timing=True))