import matplotlib.pyplot as plt
import numpy as np 
from numpy import linalg
from matplotlib import rc
import os
import subprocess
import scipy.stats as stats
import astropy.io.fits as fits
from astropy import constants as const

class Graphs(object):
	def __init__(self,title=0,xlabel=0,ylabel=0,y_names=0,y_error_names=0):
		if title != 0:
			self.title = str(title)
		else:
			self.title = r"Graph of $f\left(x\right)$"
		if xlabel != 0:
			self.xlabel = str(xlabel)
		else:
			self.xlabel = "$x$"
		if ylabel != 0:
			self.ylabel = str(ylabel)
		else:
			self.ylabel = r"$f\left(x\right)$"
		if y_names != 0:
			self.y_names = list(y_names)
		elif y_names == 0:
			pass
		if y_error_names != 0:
			self.y_error_names = str(y_error_names)
		elif y_error_names == 0:
			pass
	def create_figure_logxory(self,x_data,y_data=0,y_lim=[0,0],x_lim=[0,0],xlog=False,ylog=False,error_ydata=0,x_error=0,y_error=0):
		rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
		rc('text', usetex=True)
		x_data = np.array(x_data)
		fig = plt.figure(figsize=(16,8))
		ax = fig.add_subplot(111)
		ax.set_title(self.title,fontsize=24)
		ax.set_xlabel(self.xlabel, fontsize=20)
		ax.set_ylabel(self.ylabel, fontsize=20)
		list_of_color = []
		if y_data != 0:
			increment = float(1/float(len(y_data)+1))
			y_data = list(y_data)
			if len(y_data) == 1:
				plt.plot(x_data,y_data[0],color='g',linewidth=2,label=self.y_names[0])
			elif len(y_data) != 1:
				for i in xrange(1,len(y_data)+1):
					multiplier = float(i*increment)
					r = float(1 - multiplier)
					g = float(0 + multiplier)
					b = float(0.15 + (multiplier)/2)
					color = [r,g,b]
					list_of_color.append(color)
				for i in xrange(0,len(y_data)):
					col = tuple(list_of_color[i])
					y_names_list = self.y_names
					label = str(y_names_list[i])
					plt.plot(x_data,y_data[i],color=col,linewidth=2,label=label)
		#error plotting ===========	
		if x_error != 0:
			x_error = np.array(x_error)
			error_ydata = np.array(error_ydata)
			plt.errorbar(x_data,error_ydata,xerr = x_error,fmt='.',color='k',ecolor='b')
		elif y_error != 0:
			y_error = np.array(y_error)
			error_ydata = np.array(error_ydata)
			ax.errorbar(x_data,error_ydata,yerr=y_error,fmt='.',color='k',ecolor='b',label=self.y_error_names)
		elif y_error != 0 and x_error != 0:
			x_error = np.array(x_error)
			y_error = np.array(y_error)
			error_ydata = np.array(error_ydata)
			ax.errorbar(x_data,error_ydata,xerr=x_error,yerr=y_error,fmt='.',color='k',ecolor='b')
		#==========================
		ax.legend(bbox_to_anchor=(1.1,1.02))
		if y_lim[0] != 0 or y_lim[1] != 0:
			ax.set_ylim(y_lim)
		if x_lim[0] != 0 or x_lim[1] != 0:
			ax.set_xlim(x_lim)
		if xlog == True:
			ax.set_xscale('log')
		if ylog == True:
			ax.set_yscale('log')
		plt.grid(True)
		#plt.show()		
		return fig, ax
	def basic_plot(self,x_data=0,y_data=0,y_lim=[0,0],x_lim=[0,0]):
		rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
		rc('text', usetex=True)
		fig = plt.figure(figsize=(16,8))
		ax = fig.add_subplot(111)
		ax.set_title(self.title,fontsize=20)
		ax.set_xlabel(self.xlabel, fontsize=16)
		ax.set_ylabel(self.ylabel, fontsize=16)
		list_of_color = []	
		if y_data != 0 and x_data != 0:
			y_data = list(y_data)
			increment = float(1/len(y_data)+1)
			if len(y_data) == 1:
				plt.plot(x_data,y_data[0],'r.')
			elif len(y_data) != 1:
				for i in xrange(1,len(y_data)+1):
					multiplier = float(i*increment)
					r = float(1 - multiplier)
					g = float(0 + multiplier)
					b = float(0.15 + (multiplier)/2)
					color = [r,g,b]
					list_of_color.append(color)
				for i in xrange(0,len(y_data)):
					col = tuple(list_of_color[i])
					dummy = y_data[i]
					plt.plot(x_data,dummy,color=col,linewidth=2)
			if y_lim[0] != 0 or y_lim[1] != 0:
				ax.set_ylim(y_lim)
			if x_lim[0] != 0 or x_lim[1] != 0:
				ax.set_xlim(x_lim)
		return fig, ax


class Stats_Stuff(object):
	def __init__(self,data1,data2):
		self.data1 = list(data1)
		self.data2 = list(data2)
	def chi_squared(self):
		try:
			chi_squared = np.array([(i[0]-i[1])**2 for i in zip(self.data1,self.data2)])
			return float(np.sum(chi_squared))
		except ValueError:
			print "data sets are of unequal length"

#========================================
path_to_gelfand = '/home/dean/gelfand_pwn/2014-06-16'
phot = 'modelres.photspec.fits'
dyn = 'modelres.dyninfo.fits'
#========================================
class Physical_Graphs(object):
	def __init__(self,path_to_file=path_to_gelfand):
		if path_to_file != path_to_gelfand:
			os.chdir(path_to_file)
		else:
			os.chdir(path_to_gelfand)
		filephot = fits.open(phot)
		filedyn = fits.open(dyn)
		self.dataphot1 = filephot[1].data  
		self.dataphot2 = filephot[2].data
		self.datadyn1 = filedyn[1].data
		self.time = np.array(self.datadyn1.field(0))
	def photon_index(self,lower,upper,units,p2 = True,gammaexpected = True): #limits of plotting	
		units = str(units)
		h_special = const.h.to('{} s'.format(units)).value
		p_2 = float(2.5)*np.ones(int(self.time.size))
		gamma_expected = float(3.5/2)*np.ones(int(self.time.size))
		avfreq = np.array(self.dataphot1.field(3))
		avenerg = h_special*avfreq  
		t = 0
		indices = []
		while t < avenerg.size:
			if avenerg[t] >= float(lower) and avenerg[t] <= float(upper):
				indices.append(int(t))
			t+=1
		logavenerg = np.log(avenerg[min(indices):max(indices)+1])  
		avenerg2to10 = avenerg[min(indices):max(indices)+1]
		photon_indices = []
		deviations = []
		ones = np.ones(len(indices))
		errors = np.zeros(len(indices))
		for i in xrange(0,len(self.dataphot2)):
			luminosities = np.array(self.dataphot2[i])
			dNdE = (luminosities[min(indices):max(indices)+1]*h_special)/(const.h.to('erg s').value*avfreq[min(indices):max(indices)+1])
			logdNdE = np.log(dNdE)
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
			#finding error in gamma:
			for j in xrange(0,len(logdNdE)):
				gamma_actual = np.absolute(float((-logdNdE[j]+c)/logavenerg[j]))
				errors[j] = (np.absolute(float(gamma_actual-m))) #actual error term
			deviations.append(float(np.std(errors)))
			photon_indices.append(np.absolute(m))
		if p2 == True or gammaexpected == True:
			name = ['P_2','Expected Gamma Value']
			y_data = [p_2,gamma_expected]
			photon_index_graph = Graphs('Photon Index vs Time in {}-{} {} range'.format(lower,upper,units),'Time (years)','Photon Indices',name,y_error_names='Photon Indices')
			fig, ax = photon_index_graph.create_figure_logxory(self.time,y_data,y_lim=[1,4],error_ydata=photon_indices,y_error=deviations)
			plt.show()
		else:
			photon_index_graph = Graphs('Photon Index vs Time in {}-{} {} range'.format(lower,upper,units),'Time (years)','Photon Indices',y_error_names='Photon Indices')
			fig, ax = photon_index_graph.create_figure_logxory(self.time,y_lim=[1,4],error_ydata=photon_indices,y_error=deviations)
			plt.show()
	def total_luminosity(self,lower,upper,units): #there was a units problem. fixed 20-6-2014
		units = str(units)
		h_special = const.h.to('{} s'.format(units)).value
		avfreq = np.array(self.dataphot1.field(3))
		avenerg = h_special*avfreq  
		t = 0
		indices = []
		while t < avenerg.size:
			if avenerg[t] >= float(lower) and avenerg[t] <= float(upper):
				indices.append(int(t))
			t+=1
		logavenerg = np.log(avenerg[min(indices):max(indices)+1])  
		avenerginrange = avenerg[min(indices):max(indices)+1]
		list_of_total_luminosities = np.zeros(len(self.dataphot2))
		for j in xrange(0,len(self.dataphot2)): 
			luminosities = np.array(self.dataphot2[j])
			 #'integrating' luminosities in the 2 to 10 keV range. 
			total_luminosity = np.sum((luminosities[min(indices):max(indices)+1]*10**40)/(h_special))
			list_of_total_luminosities[j] = total_luminosity
		list_of_total_luminosities = [list_of_total_luminosities]
		name = ['Total Luminosity']
		luminosity_graph = Graphs('Total Luminosity in {}-{} {} range vs Time'.format(lower,upper,units),'Time (years)','Luminosity (ergs/s)',name)
		fig, ax = luminosity_graph.create_figure_logxory(self.time,list_of_total_luminosities,x_lim=[0,5000],ylog=True)
		plt.show()	
