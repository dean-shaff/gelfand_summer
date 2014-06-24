import matplotlib.pyplot as plt 
import numpy as np 
from numpy import linalg

import pyfits
import os
import subprocess
import scipy.stats as stats

#from astropy.constants.cgs import h #plancks constant in cgs
from plotting_tools import Graphs
#Physical Constants=====================
h = float(6.62606885e-27) #planks constant ergs*s
conversionKeV = float(624150934) #ergs to keV
h_ = float(4.135667516e-18) #plancks constant kev*s
#General Variables======================
path_to_gelfand = '/home/dean/gelfand_pwn/2014-06-16'
phot = 'modelres.photspec.fits'
dyn = 'modelres.dyninfo.fits'
#========================
'''
19-6-2014
Known issues: I'm having trouble understanding the photon index.
This is making it so figuring out the error in this term is quite difficult.
Right now I'm calculating the standard error between the model and the observed data,
instead of calculating the standard error between the calculated photon index and the real one.
I'll ask Gelfand tomorrow.
'''
'''
20-6-2014
I found out what Gelfand meant by P_2. its just a parameter that I enter into the program at the beginning.
I'm trying to figure out the error, but I seem to have a better grasp. Right now I'm calculating the standard
deviation. I dunno if thats right...
I resolved the units situation with the luminosity graph. 

I still want to ask about the units for the photon index graph and the luminosity graph. I'm not sure. 

'''
def main():
	os.chdir(path_to_gelfand)
	filephot = pyfits.open(phot)
	filedyn = pyfits.open(dyn)
	dataphot1 = filephot[1].data  
	dataphot2 = filephot[2].data 
	datadyn1 = filedyn[1].data
	time = datadyn1.field(0)
	def photon_index():
		p_2 = np.array([float(2.5) for i in time])
		gamma_expected = np.array([float(3.5/2) for i in time])
		avfreq = np.array(dataphot1.field(3))
		avenerg = np.asarray([float(i*h*conversionKeV) for i in avfreq]) #converting into keV
		t = 0
		indices = []
		k_indices = [] #finding indices around keV = 1
		while t < len(avenerg):
			if avenerg[t] >= float(2) and avenerg[t] <= float(10):
				indices.append(int(t))
			if avenerg[t] >= float(0.9) and avenerg[t] <= float(1.1):
				k_indices.append(t)
			t+=1
		logavenerg = [float(np.log(avenerg[j])) for j in indices]
		avenerg2to10 = [float(avenerg[j]) for j in indices] 
		photon_indices = []
		deviations = []
		for i in xrange(0,len(dataphot2)):
			luminosities = dataphot2[i]
			#number_photon = [float((10**40*k[0]/(conversionKeV*k[1]))) for k in zip(luminosities,avfreq)] #converting luminosity into number of photons
			logdNdE = []
			dNdE = []
			ones = []
			for j in indices:
				luminositydensity = float((luminosities[j]*h_)/(h*avfreq[j]))
				dNdE.append(luminositydensity) 
				logdNdE.append(float(np.log(luminositydensity)))
				# differencephoton = float((number_photon[j+1] - number_photon[j]))
				# differenceenerg = float((avenerg[j+1] - avenerg[j]))
				# logdNdE.append(float(np.log(np.absolute(differencephoton/differenceenerg))))
				# dNdE.append(float(np.absolute(differencephoton/differenceenerg)))
				ones.append(float(1))
			#k_actual = 	np.log((float(np.absolute(number_photon[int(k_indices[1])] - number_photon[int(k_indices[0])])))/(float(np.absolute(avenerg[int(k_indices[1])] - avenerg[int(k_indices[0])]))))
			fit_matrix = np.array(zip(logavenerg,ones))
			m,c = linalg.lstsq(fit_matrix,logdNdE)[0] #gives me the least square solution to A.x = b
			m = np.absolute(m)
			'''
			Below I make some plots to check whether my stuff is working
			'''
			def power_law_plot(j):	
				def f(t):
					return t**(-m)
				if i == int(j):
					fig = plt.figure(figsize=(13,8))
					ax = fig.add_subplot(111)
					plt.plot(avenerg2to10,dNdE,'k.')
					plt.plot(avenerg2to10,np.exp(c)*f(avenerg2to10),'b')
					plt.grid(True)
					plt.show()
			def linear_plot(j):
				if i == int(j):
					fig = plt.figure(figsize=(13,8))
					ax = fig.add_subplot(111)
					y = [float(c-m*logavenerg[t]) for t in xrange(0,len(logavenerg))]
					plt.plot(logavenerg,y,'b')
					plt.plot(logavenerg,logdNdE,'k.')
					plt.grid(True)
					plt.show()
			#power_law_plot(100)
			#linear_plot(100)
			# finding error in gamma:
			errors = []
			for j in xrange(0,len(logdNdE)):
				gamma_actual = np.absolute(float((-logdNdE[j]+c)/logavenerg[j]))
				errors.append(np.absolute(float(gamma_actual-m))) #actual error term
			deviations.append(float(np.std(errors)))
			# resetting errors, logdNdE and ones
			errors = []
			logdNdE = []
			ones = []
			photon_indices.append(np.absolute(m))
		name = ['P_2','Expected Gamma Value']
		y_data = [p_2,gamma_expected]
		photon_index_graph = Graphs('Photon Index vs Time in 2-10 keV range','Time (years)','Photon Indices',name,y_error_names='Photon Indices')
		photon_index_graph.create_figure_logxory(time,y_data,y_lim=[1,4],error_ydata=photon_indices,y_error=deviations)
	photon_index()
	def spectral_index():
		 #Lumonisity (Flux) Density L_nu = C (nu / nu_0) ^ alpha
		 # log(L_nu) = log(C) + alpha*(log(nu/nu_0))
		 nu_0 = float(10**9) #GHz 
		 av_freq = dataphot1.field(3)
		 av_freq_radio = [i for i in av_freq if i >= 10**9 and i <= 10**10]
		 indices_radio = [int(i) for i in xrange(0,len(av_freq)) if av_freq[i] >= 10**9 and av_freq[i] <= 10**10]
		 log_radio = [float(np.log(i/nu_0)) for i in av_freq_radio]
		 log_radio = np.array(log_radio)
		 #empty lists
		 error = []
		 alphas = []
		 deviations = []
		 for j in xrange(0,len(dataphot2)):
		 	luminosities = dataphot2[j]
		 	luminositiesradio = np.asarray([luminosities[i] for i in indices_radio])
		 	logluminosities = np.asarray([np.log(luminosities[i]) for i in indices_radio])
		 	ones = [1 for i in indices_radio]
		 	dummy = np.vstack((log_radio,ones))
		 	fit_matrix = np.transpose(dummy)
		 	m,c = linalg.lstsq(fit_matrix,logluminosities)[0]
		 	#Checking======================
		 	def plot_log(t):
		 		if int(j) == int(t):
			 		fig = plt.figure(figsize=(14,8))
			 		ax = fig.add_subplot(111)
			 		plt.plot(log_radio,c+(m*log_radio),'b')
			 		plt.plot(log_radio,logluminosities,'k.')
			 		plt.grid(True)
			 		plt.show()
			def plot_powerlaw(t):
				avfreq_radio_norm = [i/nu_0 for i in av_freq_radio]
				if int(j) == int(t):
					fig = plt.figure(figsize=(14,8))
					ax = fig.add_subplot(111)
					plt.plot(av_freq_radio,luminositiesradio,'k.')
					plt.plot(av_freq_radio,np.exp(c)*((avfreq_radio_norm)**m),'b')
					plt.grid(True)
					plt.show()
			plot_log(100)
			plot_powerlaw(100)
			#===============================
			#Error==========================
			for i in xrange(0,len(logluminosities)):
				alpha_actual = (logluminosities[i] - c)/log_radio[i]
				error.append(float(np.absolute(alpha_actual-m)))
			deviations.append(float(np.std(error)))	
			error = []
		 	alphas.append(np.absolute(m))
		 name = ['Spectral Index']
		 y_data = [alphas]
		 spectral_index_graph = Graphs('Spectral Index vs Times', 'Time (years)','Spectral Index (unitless)',y_error_names='Spectral Index')
		 spectral_index_graph.create_figure_logxory(time,error_ydata=alphas,y_error=deviations)

	#spectral_index()
	def luminosity2to10(): #there was a units problem. fixed 20-6-2014
		avfreq = dataphot1.field(3)
		avenerg = [float(i*h*conversionKeV) for i in avfreq] #converting into keV
		t = 0
		indices = []
		while t < len(avenerg):
			if avenerg[t] >= 2 and avenerg[t] <= 10:
				indices.append(int(t))
			t+=1
		total_luminosity = 0
		list_of_total_luminosities = []
		for j in xrange(0,len(dataphot2)): 
			luminosities = dataphot2[j]
			for i in indices: #'integrating' luminosities in the 2 to 10 keV range. 
				total_luminosity += (float(luminosities[i]*10**40/(h*conversionKeV)))
			list_of_total_luminosities.append(total_luminosity)
			total_luminosity = 0
		list_of_total_luminosities = [list_of_total_luminosities]
		name = ['Total Luminosity']
		luminosity_graph = Graphs('Total Luminosity in 2-10 keV range vs Time','Time (years)','Luminosity (ergs/s)',name)
		luminosity_graph.create_figure_logxory(time,list_of_total_luminosities,x_lim=[0,30000],ylog=True)
	#luminosity2to10()
main()


