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
#Extra/Calculated Parameters===============
tstep = -1 #time step (only takes integer values) 21-6-2014 changed tstep from 1000 to 100
age = float(((2*char_age)/(brakind-1))-tau)#(?) age of system #says age > 29000 (?) 
e0 = float(edot*(1+(age/tau))**((brakind+1)/(brakind-1))) #initial spin-down luminosity (10^37 ergs/s)
velpsr = 0 #update 16-6-2014 - velocity is zero
f_max = 0 #fraction in maxwellian component
kT_max = 0 #energy of maxwellian component
nic = 0 #number of background photon field
ictemp = 0 #temperature of background photon field
icnorm = 0 #normalization of background photon field
dynstep = 0 #[optional]
elecstep = 0 #[optional]
photstep = 0 #[optional]
#Code======================
mcmc_path = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc'
testing_path = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing'

data = [d, radio1, radio2, radio3, radio4, fluxsoftx, 
	gammasoftx, fluxhardx, gammahardx, gammagamma, gamma1] 
dataerror=[dsigma, radio1sigma, radio2sigma, radio3sigma, 
	radio4sigma, fluxsoftxsigma, fluxhardxsigma, gammahardxsigma, 
	gammagammasigma, gamma1sigma] 

# runner = Output()
# runner.gen_output(tstep,esn,mej,nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic,ictemp,icnorm)

def lnlike(theta,data,dataerror,testing=False):
	
	[d, radio1, radio2, radio3, radio4, fluxsoftx, 
	gammasoftx, fluxhardx, gammahardx, gammagamma, gamma1] = data
	[dsigma, radio1sigma, radio2sigma, radio3sigma, 
	radio4sigma, fluxsoftxsigma, fluxhardxsigma, gammahardxsigma, 
	gammagammasigma, gamma1sigma] = dataerror
	#underscores is so I can distinguish between starting values and not. 
	[esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_, 
	ebreak_, p1_, p2_] = theta

	if testing == False:
		runner = Output()
		age_ = float(((2*char_age)/(brakind_-1))-tau_)#(?) age of system #says age > 29000 (?) 
		e0_ = float(edot*(1+(age_/tau_))**((brakind_+1)/(brakind_-1))) #initial spin-down luminosity (10^37 ergs/s)
		velpsr = 0 #update 16-6-2014 - velocity is zero
		f_max = 0 #fraction in maxwellian component
		kT_max = 0 #energy of maxwellian component
		nic = 0 #number of background photon field
		ictemp = 0 #temperature of background photon field
		icnorm = 0 #normalization of background photon field
		runner.gen_output(tstep,esn_,mej_,nism_,brakind_,tau_,age_,e0_,velpsr,etag_,
			etab_,emin_,emax_,ebreak_,p1_,p2_,f_max,kT_max,nic,ictemp,icnorm,directory_path=testing_path)
	else: 
		pass

	phot = 'modelres.photspec.fits'
	dyn = 'modelres.dyninfo.fits'
	elec = 'modelres.elecspec.fits'
	
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
	for i in xrange(1,len(data)-1): #not including distance
		coeff = np.log(1.0/(np.sqrt(2*np.pi)*dataerror[i]))
		chisqr = ((model[i-1] - data[i])**2)/(dataerror[i])
		total += coeff*chisqr
	
	print('time in calculation: {}'.format(time.time()-t))
	return -0.5*total

def lnprior(theta):
	esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_,ebreak_, p1_, p2_ = theta
	if mej_ > 0 and brakind_ > 0 and tau_ > 0 and esn_ > 0 and nism_ > 0 and etag_ >= 0 and etag_ < 1 and emin_ > 0 and emax_ > 0 and p1_ > 0 and p2_ > 0 and etab_ > 0:
		return 0 #at least until Gelfand provides me with some priors	
	else: 
		return -np.inf

number_functioncall = []
def lnprob(theta,data,dataerror):
	number_functioncall.append(1)
	print(len(number_functioncall))
	if len(number_functioncall) <= 5:
		esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_,ebreak_, p1_, p2_ = theta
		lp = lnprior(theta)
		if not np.isfinite(lp):
			return -np.inf
		return lp + lnlike(theta,data,dataerror)
	else:

		return np.nan
		
jump = 1
def callbackF(theta):
	esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_,ebreak_, p1_, p2_ = theta
	global jump 
	print("{} {} {} {} {} {} {} {} {} {} {} {} {}".format(jump, esn_, mej_, nism_, brakind_, tau_, etag_, etab_, emin_, emax_,ebreak_, p1_, p2_))
	jump += 1

def optimize_lnprob():
	nll = lambda *args: -lnprob(*args)
	result = op.minimize(nll, [esn, mej, nism, brakind, tau, etag, etab, emin, emax, ebreak, p1, p2],
						 args=(data, dataerror), method='Powell',options={'disp':True,'maxfev':5},callback=callbackF)
	esn_ml, mej_ml, nism_ml, brakind_ml, tau_ml, etag_ml, etab_ml, emin_ml, emax_ml,ebreak_ml, p1_ml, p2_ml = result['x']
	print result['success']
	print lnlike([esn_ml, mej_ml, nism_ml, brakind_ml, tau_ml, etag_ml, etab_ml, emin_ml, emax_ml,ebreak_ml, p1_ml, p2_ml],data,dataerror)
	return [esn_ml, mej_ml, nism_ml, brakind_ml, tau_ml, etag_ml, etab_ml, emin_ml, emax_ml,ebreak_ml, p1_ml, p2_ml]

best_fit = optimize_lnprob()
print(best_fit)

# print lnprob([esn, mej, nism, brakind, tau, etag, etab, emin, emax, 
# 	ebreak, p1, p2],[d, radio1, radio2, radio3, radio4, fluxsoftx, 
# 	gammasoftx, fluxhardx, gammahardx, gammagamma, gamma1],[dsigma, radio1sigma, radio2sigma, radio3sigma, 
# 	radio4sigma, fluxsoftxsigma, fluxhardxsigma, gammahardxsigma, 
# 	gammagammasigma, gamma1sigma])

#==============================================
def run_emcee():
	ndim, nwalkers = 12, 100
	pos = [[esn, mej, nism, brakind, tau, etag, etab, emin, emax, 
		ebreak, p1, p2] + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]
	sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(data,dataerror))
	sampler.run_mcmc(pos, 500)
#run_emcee()






# theta1 = [1.7002174640867751, 8.0016364987364543, 0.99877967608877527, 1.0255358037568771, 502.58792896154586, 2.5879289615458418, 2.5889289615458417,
#  3.5879289615458418, 10000002.587928962, 10002.587928961546, 4.0879289615458418, 5.0879289615458418]

# print(lnlike(theta1,data,dataerror))

# [3.5879289615458418, 10.587928961545842, 3.5879289615458418, 5.5879289615458418, 502.58792896154586, 2.5879289615458418, 2.5889289615458417, 3.5879289615458418, 10000002.587928962, 10002.587928961546, 4.0879289615458418, 5.0879289615458418]

