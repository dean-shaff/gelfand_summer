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
#Data===========================
radius_pwn = 40 # "
radius_snr = 150 # "
edot = 3.3 #(10^37 ergs/s) current spin down luminosity
p = 61.86 # ms period
d = 4.7 
dsigma = 0.4 # distance kpc
ex_vel = 38.39 
ex_velsigma = 6.75 # angular expansion mas/yr
radio1 = 7 
radio1sigma = 0.4 # 1.43 GHz flux density Jy
radio2 = 6.7 
radio2sigma = 0.3 # 4.7 GHz flux density Jy
radio3 = 5.6 
radio3sigma = 0.3 # 15 GHz flux density Jy
radio4 = 3.9 
radio4sigma = 0.7 # 84.2 GHz flux density Jy
fluxsoftx = 7.5 
fluxsoftxsigma = 0.1 # GUESSING SIGMA 0.5-10 keV unabsorbed flux *10**-11 erg/(s*cm^2)
gammasoftx = 1.89 
gammasoftxsigma = 0.02 #using obsid 1233 0.5-10 keV photon index. unitless
fluxhardx = 5.2 
fluxhardxsigma = 0.1 # GUESSING SIGMA 20-100 keV unabsorbed flux *10**-11 erg/(s*cm^2)
gammahardx = 2.2 
gammahardxsigma = 0.1 #20-100 keV photon index
gammagamma = 2.08 
gammagammasigma = 0.22 # 1-10 TeV photon index
gamma1 = 4.59 
gamma1sigma = 1.00 # 1 TeV photon density x 10^-13 photons/(TeV*s*cm^2)

char_age = 4850 #yr
edot = 3.3 #(10^37 ergs/s)
#Fit Parameters=====================
'''
I've initialized these values to the ones that I used earlier in the summer.
'''
esn = 1 #supernova explosion energy
mej = 8 #ejecta mass
nism = 0.001 #ISM density #low nism gives drastically lower chisquare
brakind = 3 #braking index
tau = 500 #spin-down timescale
etag = 0 #(?) fraction of spin-down luminosity lost as radiation #update 16-6-2014 - set this to zero
etab = 0.001 #magnetization of PW
emin =  1 #minimum particle energy 
emax = 1e6 #maximum particle energy 
ebreak = 1e3 #break energy in PW
p1 = 1.5 #below the break
p2 = 2.5 #above the break

#[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5]
theta_list = [[1,8,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[0.1,8,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[10,8,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[1,3,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],
			[1,15,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[1,8,0.001,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[1,8,100,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[1,8,1,2,500,0,0.001,1,1e6,1e3,1.5,2.5],
			[1,8,1,3,10,0,0.001,1,1e6,1e3,1.5,2.5],[1,8,1,3,1e4,0,0.001,1,1e6,1e3,1.5,2.5],[1,8,1,3,500,0,0.0001,1,1e6,1e3,1.5,2.5],[1,8,1,3,500,0,0.1,1,1e6,1e3,1.5,2.5],
			[1,8,1,3,500,0,0.001,51*1e-6,1e6,1e3,1.5,2.5],[1,8,1,3,500,0,0.001,10,1e6,1e3,1.5,2.5]]

theta_list2 = [[1,15,0.001,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[1, 8, 0.0001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[1, 8, 0.01, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],
				[1, 15, 0.0001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[1, 15, 0.01, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5]]
#last two are preferred from intial run[1,8,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[1,15,1,3,500,0,0.001,1,1e6,1e3,1.5,2.5],

theta_list3 = [[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[1, 3, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],
				[1, 8, 0.005, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[1, 8, 0.0005, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5]]

theta_list4 = [[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[10, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],
				[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.0, 2.5],[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.9, 2.5],
				[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.1],[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 3.0]]
theta_output = [[1, 8, 0.001, 3, 500, 0, 0.001, 1, 1000000.0, 1000.0, 1.5, 2.5],[-3.187357049359683, 10.587928961545842, 2.5889289615458417, 5.5879289615458418, 502.58792896154586, 2.5879289615458418, 2.5889289615458417, 
				3.5879289615458418, 1000002.5879289615, 1002.5879289615458, 4.0879289615458418, 5.0879289615458418]]

# theta_ml = [  2.68514901e+00   1.05701937e+01   2.58892896e+00   5.53920354e+00
#    4.54232639e+01   2.92055684e+01   2.92065684e+01   3.02055684e+01
#    1.00002921e+06   1.02920557e+03   3.07055684e+01   3.17055684e+01]
# #Extra/Calculated Parameters===============
# tstep = -1 #time step (only takes integer values) 21-6-2014 changed tstep from 1000 to 100
# age = float(((2*char_age)/(brakind-1))-tau)#(?) age of system #says age > 29000 (?) 
# e0 = float(edot*(1+(age/tau))**((brakind+1)/(brakind-1))) #initial spin-down luminosity (10^37 ergs/s)
# velpsr = 0 #update 16-6-2014 - velocity is zero
# f_max = 0 #fraction in maxwellian component
# kT_max = 0 #energy of maxwellian component
# nic = 0 #number of background photon field
# ictemp = 0 #temperature of background photon field
# icnorm = 0 #normalization of background photon field
# dynstep = 0 #[optional]
# elecstep = 0 #[optional]
# photstep = 0 #[optional]
#Code======================
mcmc_path = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc'
testing_path = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing'

data = [d, radio1, radio2, radio3, radio4, fluxsoftx, 
	gammasoftx, fluxhardx, gammahardx, gammagamma, gamma1] 
data_names = ['radio1', 'radio2', 'radio3', 'radio4', 'fluxsoftx', 
	'gammasoftx', 'fluxhardx', 'gammahardx', 'gammagamma', 'gamma1']
dataerror=[dsigma, radio1sigma, radio2sigma, radio3sigma, 
	radio4sigma, fluxsoftxsigma, fluxhardxsigma, gammahardxsigma, 
	gammagammasigma, gamma1sigma] 

def chisqr(theta): #,data,dataerror,testing=False):
	data = [d, radio1, radio2, radio3, radio4, fluxsoftx, 
	gammasoftx, fluxhardx, gammahardx, gammagamma, gamma1] 
	dataerror = [dsigma, radio1sigma, radio2sigma, radio3sigma, 
	radio4sigma, fluxsoftxsigma, fluxhardxsigma, gammahardxsigma, 
	gammagammasigma, gamma1sigma] 
	#underscores is so I can distinguish between starting values and not. 
	[esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_, 
	ebreak_, p1_, p2_] = theta

	if mej_ < 0 or brakind_ < 0 or tau_ < 0 or esn_ < 0 or nism_ < 0 or etag_ <= 0 and etag_ > 1 or emin_ < 0 or emax_ < 0 or p1_ < 0 or p2_ < 0 or etab_ < 0 or p1_ > 3:
		print("Parameters out of range")
		return np.inf

	runner = Output()
	age_ = float(((2*char_age)/(brakind_-1))-tau_)#(?) age of system #says age > 29000 (?) 
	e0_ = float(edot*(1+(age_/tau_))**((brakind_+1)/(brakind_-1))) #initial spin-down luminosity (10^37 ergs/s)
	velpsr = 0 #update 16-6-2014 - velocity is zero
	f_max = 0 #fraction in maxwellian component
	kT_max = 0 #energy of maxwellian component
	nic = 0 #number of background photon field
	ictemp = 0 #temperature of background photon field
	icnorm = 0 #normalization of background photon field
	tstep = -1

	phot = 'modelres.photspec.fits'
	dyn = 'modelres.dyninfo.fits'
	elec = 'modelres.elecspec.fits'

	# if testing == True:
	# 	runner.gen_output(tstep,esn_,mej_,nism_,brakind_,tau_,age_,e0_,velpsr,etag_,
	# 		etab_,emin_,emax_,ebreak_,p1_,p2_,f_max,kT_max,nic,ictemp,icnorm,directory_path=testing_path)
	# 	assert os.path.exists("{}/{}".format(testing_path,phot))==True, "Make sure to generate fits files!"

	# elif testing == False:
	runner.gen_output(tstep,esn_,mej_,nism_,brakind_,tau_,age_,e0_,velpsr,etag_,
		etab_,emin_,emax_,ebreak_,p1_,p2_,f_max,kT_max,nic,ictemp,icnorm,directory_path=mcmc_path)	
	assert os.path.exists("{}/{}".format(mcmc_path,phot))==True, "Make sure to generate fits files!"
	t = time.time()
	reader = Observables(phot,dyn,elec)
	radio1model = reader.grab_flux_density(1.43, 'GHz', d)
	radio2model = reader.grab_flux_density(4.7, 'GHz', d)
	radio3model = reader.grab_flux_density(15, 'GHz', d)
	radio4model = reader.grab_flux_density(84.2, 'GHz', d)
	fluxsoftxmodel = reader.grab_total_flux(0.5,10,'keV',d)
	gammasoftxmodel = reader.photon_index(0.5,10,'keV')
	fluxhardxmodel = reader.grab_total_flux(20,100,'keV',d)
	gammahardxmodel = reader.photon_index(20,100,'keV')
	gammagammamodel = reader.photon_index(1,10,'TeV')
	gamma1model = reader.photon_density(1,'TeV',d)
	model = [radio1model,radio2model,radio3model,radio4model,fluxsoftxmodel,
		gammasoftxmodel,fluxhardxmodel,gammahardxmodel,gammagammamodel,gamma1model]
	total = 0
	list_of_differences = []
	with open('log1wed.txt','a') as file1:
		for i in xrange(1,len(data)-1): #not including distance
			file1.write("{} : {}\n".format(data_names[i-1],model[i-1]-data[i]))
			list_of_differences.append(model[i-1]-data[i])
			chisqr = ((model[i-1] - data[i])**2)/(dataerror[i])
			lncoeff = np.log(1.0/(np.sqrt(2*np.pi)*dataerror[i]))
			total += chisqr*lncoeff
		file1.write("{}\n".format(theta))
	#print('time in calculation: {}'.format(time.time()-t))
		file1.write("{}\n\n".format(0.5*total))
	return 0.5*total#, list_of_differences #I want to minimize the negative liklihood...

# with open('log5tues.txt','w') as file1:
# 	for i in theta_output:
# 		print(i)
# 		chisqur, listdiff = chisqr(i,data,dataerror)
# 		print(chisqur)
# 		file1.write('{}\n'.format(i))
# 		file1.write('{}\n{}\n\n'.format(chisqur, listdiff))

jump = 1
def callbackF(theta):
	esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_,ebreak_, p1_, p2_ = theta
	global jump 
	print("{} {} {} {} {} {} {} {} {} {} {} {} {}".format(jump, esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_,ebreak_, p1_, p2_))
	jump += 1

def optimize_chisqr():
	#nll = lambda *args: chisqr(*args)
	result = op.minimize(chisqr, [esn, mej, nism, brakind, tau, etag, etab, emin, emax, ebreak, p1, p2],
						method='Powell',options={'disp':True},callback=callbackF)
	esn_ml, mej_ml, nism_ml, brakind_ml, tau_ml, etag_ml, etab_ml, emin_ml, emax_ml,ebreak_ml, p1_ml, p2_ml = result['x']
	print result['success']
	print chisqr([esn_ml, mej_ml, nism_ml, brakind_ml, tau_ml, etag_ml, etab_ml, emin_ml, emax_ml,ebreak_ml, p1_ml, p2_ml])
	return [esn_ml, mej_ml, nism_ml, brakind_ml, tau_ml, etag_ml, etab_ml, emin_ml, emax_ml,ebreak_ml, p1_ml, p2_ml]

best_fit = optimize_chisqr()
print(best_fit)