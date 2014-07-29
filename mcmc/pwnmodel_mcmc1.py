#program that runs pwn model
import os
import subprocess
import time
import datetime
import numpy as np
import astropy.io.fits as fits
import astropy.units as u 
from astropy import constants as const
from numpy import linalg
import time
#=========================================
path_to_pwn = '/home/dean/gelfand_pwn'
mcmc_path = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc'

#=========================================
class Output(object):
	def __init__(self):
		pass
	def gen_output(self,tstep,esn,mej,
			nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic,ictemp,icnorm,dynstep=False,elecstep=False,photstep=False,directory_path=False):
		t = float(time.time()) #just so I can get the timing... I want to start a big csv file that has ALL my runtimes...
		filename = str(datetime.datetime.today())
		os.chdir(path_to_pwn)
		if dynstep==False and elecstep==False and photstep==False:
			call = './pwnmodel.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(tstep,esn,mej,
				nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic,ictemp,icnorm)
		else:
			call = './pwnmodel.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(tstep,esn,mej,
				nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic, ictemp, icnorm, dynstep, elecstep, photstep)
		subprocess.call(call,shell=True)
		print("time in calculation: {}".format(float(time.time()) - t))
		if directory_path == False:
			subprocess.call('mv *.fits {}'.format(mcmc_path),shell = True)
			os.chdir(mcmc_path) 
		elif directory_path != False:
			subprocess.call('mv *.fits {}'.format(directory_path),shell = True)
			os.chdir(directory_path) 
		

	def delete_fits(self):
		os.chdir(mcmc_path)
		subprocess.call('rm *.fits',shell=True)

class Observables(object):
	def __init__(self,photospec,dyninfo,elecspec):
		self.phot = photospec
		self.dyn = dyninfo
		self.elec = elecspec
	def photon_index(self,lower,upper,units,timing=False):
		units = str(units)
		h_special = const.h.to('{} s'.format(units)).value
		try:
			t1 = time.time()
			filephot = fits.open(self.phot)
			dataphot1 = filephot[1].data
			dataphot2 = filephot[2].data
			avfreq = np.array(dataphot1.field(3))
			avenerg = h_special*avfreq  
			t = 0
			indices = []
			while avenerg[t] < upper: #to make the search shorter. no need to search entire list.
				if avenerg[t] >= float(lower) and avenerg[t] <= float(upper):
					indices.append(int(t))
				t+=1
			logavenerg = np.log(avenerg[min(indices):max(indices)+1]) 
			avenergrange = avenerg[min(indices):max(indices)+1]
			ones = np.ones(len(indices))
			luminosities = np.array([float(dataphot2.field(i)) for i in indices])  #wtf... 
			dNdE = (luminosities*h_special)/(const.h.to('erg s').value*avfreq[min(indices):max(indices)+1])
			logdNdE = np.log(dNdE)
			fit_matrix = np.array(zip(logavenerg,ones))
			m,c = linalg.lstsq(fit_matrix,logdNdE)[0] #gives me the least square solution to A.x = b	
			
			if timing == True:
				print("Time calculating photon index: {}".format(time.time()-t1))
			
			return np.absolute(m)
		except IOError:
			print("You need to generate fits files")

	def photon_density(self, value, units, d,timing=False):
		units = str(units)
		h_special = const.h.to('{} s'.format(units)).value
		try:
			t1 =time.time()
			filephot = fits.open(self.phot)
			dataphot1 = filephot[1].data
			dataphot2 = filephot[2].data
			avfreq = np.array(dataphot1.field(3))
			avenerg = h_special*avfreq 

			def search(threshold):
				indices = []
				for i,j in enumerate(avenerg):
					if j <= value + threshold and j >= value - threshold:
						indices.append(i)
					else:
						pass
				return indices

			threshold = 0.05*value
			indices = search(threshold)
			t = 1.01
			if len(indices) == 0:
				while len(indices) == 0:
					threshold *= t
					indices = search(threshold)
			assert avenerg[min(indices)] <= value + threshold and avenerg[min(indices)] >= value - threshold, 'Your search didn\'t work'
			#units_flux = (10**40*u.erg)/(u.s*u.Hz*u.cm**2)
			distance = d*u.kpc.to(u.cm)
			energyphoton = avfreq[min(indices)]*(const.h.to('erg s').value)
			luminosities = np.array([float(dataphot2.field(i)) for i in indices])
			flux_density = (luminosities[0]*10**40)/(4*np.pi*(distance**2))
			if timing == True:
				print("Time calculating photon density: {}".format(time.time()-t1))
			return (flux_density/(energyphoton*h_special))/(10**-13) #for correct scaling

		except IOError:
			print("You need to generate fits files")

	def grab_flux_density(self,value,units,d,timing=False): #d for distance 
		'''
		Here I'm basically assuming that the user will be providing a radio frequency, as in GHz.
		I don't have this set up to work with energies
		'''
		units = str(units)
		#h_special = const.h.to('{} s'.format(units)).value
		try:
			t1 = time.time()
			filephot = fits.open(self.phot)
			dataphot1 = filephot[1].data
			dataphot2 = filephot[2].data
			luminosities = dataphot2[0]
			
			if units != 'Hz':
				conversion = u.Hz.to(units)
				avfreq = np.array(dataphot1.field(3))*conversion
			else:
				avfreq = np.array(dataphot1.field(3))
			flux = 0

			def search(threshold):
				indices = []
				for i,j in enumerate(avfreq):
					if j <= value + threshold and j >= value - threshold:
						indices.append(i)
					else:
						pass
				return indices

			threshold = 0.05*value
			indices = search(threshold)

			t = 1.01
			if len(indices) == 0:
				while len(indices) == 0:
					threshold *= t
					indices = search(threshold)
			assert avfreq[min(indices)] <= value + threshold and avfreq[min(indices)] >= value - threshold, 'Your search didn\'t work'
			if len(indices) != 1:
				flux = luminosities[indices[0]]
			elif len(indices) == 1:
				flux = luminosities[indices[0]]
			else:
				pass
			distance = d*u.kpc.to(u.cm)
			unit_flux = (10**40*u.erg)/(u.s*u.Hz*(u.cm**2)*4*np.pi*(distance**2))
			if timing == True:
				print("Time calculating flux density: {}".format(time.time()-t1))
			return (flux*unit_flux).to('Jy').value
		except IOError:
			print("You need to generate fits files")

	def grab_total_flux(self,lower,upper,units,d,timing=False):
		units = str(units)
		h_special = const.h.to('{} s'.format(units)).value
		try:
			t1 = time.time()
			filephot = fits.open(self.phot)
			dataphot1 = filephot[1].data
			dataphot2 = filephot[2].data
			avfreq = np.array(dataphot1.field(3))
			avenerg = avfreq*h_special
			t = 0
			indices = []
			while t < avenerg.size:
				if avenerg[t] >= float(lower) and avenerg[t] <= float(upper):
					indices.append(int(t))
				t+=1
			luminosities = np.array([float(dataphot2.field(i)) for i in indices])
			distance = d*u.kpc.to(u.cm)
			unit_flux = (10**40*u.erg)/(u.s*u.Hz*(u.cm**2)*4*np.pi*(distance**2)) 
			#flux_units converts from total flux to flux density
			if timing == True:
				print("Time calculating total flux: {}".format(time.time()-t1))
			return (np.sum(luminosities)*unit_flux.value)/((10**-11)*h_special)

		except IOError:
			print("You need to generate fits files")
