#Dean Shaff 16/6/2014
#Running Professor Gelfands PWN program and then making some graphs
import os
import matplotlib.pyplot as plt 
import numpy as np 
import pyfits
import subprocess
import datetime
from plotting_tools import Graphs 
import time
#Parameters=====================
tstep = 1000 #time step (only takes integer values)
esn = 1 #supernova explosion energy
mej = 8 #ejecta mass
nism = 1 #ISM density 
brakind = 3 #braking index
tau = 500 #spin-down timescale
age = 100000 #(?) age of system #says age > 29000 (?)
e0 = 1000 #initial spin-down luminosity (10^37 ergs/s)
velpsr = 0 #update 16-6-2014 - velocity is zero
etag = 0 #(?) fraction of spin-down luminosity lost as radiation #update 16-6-2014 - set this to zero
etab = 0.001 #magnetization of PW
emin =  1 #minimum particle energy 
emax = 10e6 #maximum particle energy
ebreak = 10e3 #break energy in PW
p1 = 1.5 #below the break
p2 = 2.5 #above the break
f_max = 0 #fraction in maxwellian component
kT_max = 0 #energy of maxwellian component
nic = 0 #number of background photon field
ictemp = 0 #temperature of background photon field
icnorm = 0 #normalization of background photon field
dynstep = 0 #[optional]
elecstep = 0 #[optional]
photstep = 0 #[optional]
#General Variables========================
date_original = '2014-06-16'
path_to_pwn = '/home/dean/gelfand_pwn'
#=========================================
def main():
	date = str(datetime.date.today())
	os.chdir(path_to_pwn)
	subprocess.call('./pwnmodel.exe %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r' %(tstep,esn,mej,
		nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic),shell=True)
	subprocess.call('mkdir %s' %date,shell=True)
	subprocess.call('mv *.fits %s/%s' % (path_to_pwn,date),shell = True) 

def radius_graph():
	os.chdir('%s/%s'%(path_to_pwn,date_original))
	dyndata = pyfits.open('modelres.dyninfo.fits')
	datadyn = dyndata[1].data
	time = datadyn.field(0)
	pwnrad = datadyn.field(1)
	snrrad = datadyn.field(2)
	reverseshock = datadyn.field(3)
	names = ['PWN radius','SNR radius', 'Reverse Shock']
	list_of_radii = [pwnrad,snrrad,reverseshock]
	radii_graph = Graphs('Radii vs Time (xlog)','Time (years)','Distance (parsecs)',names)
	radii_graph.create_figure_logxory(time,list_of_radii,y_lim=[-5,30],x_lim=[1,1e5],xlog=True)
	
def luminosity_graph(): #should I do a logarithmic scale?
	os.chdir('%s/%s'%(path_to_pwn,date_original))
	photdata = pyfits.open('modelres.photspec.fits')
	phot1 = photdata[1].data
	phot2 = photdata[2].data
	avfreq = list(phot1.field(3))
	avfreq.insert(0,0) #the frequency and luminosity sets aren't the same length
	total_timesteps = int(len(phot2)) #I know len() outputs an integer, but this is just for me to remember
	lum1 = [i[0]*i[1] for i in zip(avfreq,phot2[1])] #scaling
	lum2 = [i[0]*i[1] for i in zip(avfreq,phot2[int(total_timesteps/2)])]
	lum3 = [i[0]*i[1] for i in zip(avfreq,phot2[total_timesteps-1])]
	lum_data = [lum1,lum2,lum3]
	names = ['Luminosity at time = %r' %(100),'Luminosity at time = %r' %(100*(int(total_timesteps/2))),'Luminosity at time = %r' %(total_timesteps*100)]
	luminosity_graph = Graphs('Luminosity vs Average Frequency (log-log)','Average Frequency (Hz)','Luminosity*Frequency (Ergs/s)',names)
	luminosity_graph.create_figure_logxory(avfreq,lum_data,xlog=True,ylog=True)

def elec_graph():
	os.chdir('%s/%s'%(path_to_pwn,date_original))
	elecdata = pyfits.open('modelres.elecspec.fits')
	elec1 = elecdata[1].data
	elec2 = elecdata[2].data
	avE = list(elec1.field(3))
	total_timesteps = int(len(elec2))
	electron1 = []
	electron2 = []
	electron3 = []
	for i in xrange(0,len(avE)-1):
		time1 = elec2[1]
		time2 = elec2[int(total_timesteps/2)]
		time3 = elec2[total_timesteps-1]
		difference = float(avE[i+1]-avE[i])
		electron1.append((float(avE[i]**2)*(time1[i]/difference)))
		electron2.append((float(avE[i]**2)*(time2[i]/difference)))
		electron3.append((float(avE[i]**2)*(time3[i]/difference)))
	avE.pop(len(avE)-1) #to make electron lists and avE the same size
	electron_data = [electron1,electron2,electron3]
	names = ['Number of Electrons per Energy at time = %r' %(100),'Number of Electrons per Energy at time = %r' %(100*(int(total_timesteps/2))),
		'Number of Electrons per Energy at time = %r' %(100*total_timesteps)]
	electron_graph = Graphs('Number of Electrons per Energy vs Energy (log-log)','Average Energies (ergs)','Electrons per energy (ergs)',names)
	electron_graph.create_figure_logxory(avE,electron_data,[1e-2,1e13],xlog=True,ylog=True)

#radius_graph()
luminosity_graph()
#elec_graph()

