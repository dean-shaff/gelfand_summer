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
path_to_speed = '/home/dean/gelfand_pwn/speedup'
path_default = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/default_fits'
#=========================================

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
			# lower_con = avenerg >= float(lower)
			# upper_con = avenerg <= float(upper)
			t = 0
			indices = []
			while t < avenerg.size:
				if avenerg[t] >= float(lower) and avenerg[t] <= float(upper):
					indices.append(int(t))
				t+=1
			luminosities = np.array([float(dataphot2.field(i)) for i in indices])#xrange(0,avenerg.size-1)])
			# luminosities = luminosities[lower_con*upper_con]
			distance = d*u.kpc.to(u.cm)
			unit_flux = (10**40*u.erg)/(u.s*u.Hz*(u.cm**2)*4*np.pi*(distance**2)) 
			#flux_units converts from total flux to flux density
			if timing == True:
				print("Time calculating total flux: {}".format(time.time()-t1))
			return (np.sum(luminosities)*unit_flux.value)/((10**-11)*h_special)

		except IOError:
			print("You need to generate fits files")

	def radius_info(self):
		try:
			filedyn = fits.open(self.dyn)
			datadyn1 = filedyn[1].data
			time = np.array(datadyn1.field(0))
			radius = np.array(datadyn1.field(1))
			assert len(time) > 1, "Rerun code with tstep != -1" 
			return time, radius
		except IOError:
			print("You need to generate fits files")