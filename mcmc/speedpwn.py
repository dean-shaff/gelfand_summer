'''
I want to make Gelfand's code run faster. I'm going to modify
certain parameters in his code to try and speed things up. 
I'm going to start by making a baseline graph of radius vs time. 

pwnmodel.exe tstep esn mej nism brakind tau age e0 velpsr etag etab emin emax ebreak p1 p2 f_max kT_max nic ictemp(s) icnorm(s) [dynstep elecstep photstep]

'''
import matplotlib.pyplot as plt

from pwnmodel_mcmc1 import Output
from pwnmodel_mcmc1 import Observables
import numpy as np 
from plotting_tools_mcmc import Graphs
import os
# ============================================
phot = 'modelres.photspec.fits'
dyn = 'modelres.dyninfo.fits'
elec = 'modelres.elecspec.fits'
directory_test = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/speedtests'

char_age = 4850 #yr
edot = 3.3 #(10^37 ergs/s)
d = 4.7 
dsigma = 0.4
esn_ = 1 #supernova explosion energy
mej_ = 8 #ejecta mass
nism_ = 0.001 #ISM density #low nism gives drastically lower chisquare
brakind_ = 3 #braking index
tau_ = 500 #spin-down timescale
etag_ = 0 #(?) fraction of spin-down luminosity lost as radiation #update 16-6-2014 - set this to zero
etab_ = 0.001 #magnetization of PW
emin_ =  1 #minimum particle energy 
emax_ = 1e6 #maximum particle energy 
ebreak_ = 1e3 #break energy in PW
p1_ = 1.5 #below the break
p2_ = 2.5 #above the break
age_ = float(((2*char_age)/(brakind_-1))-tau_)#(?)  
e0_ = float(edot*(1+(age_/tau_))**((brakind_+1)/(brakind_-1))) #initial spin-down luminosity (10^37 ergs/s)
# (4350.0, 310.49699999999996)
velpsr = 0 #update 16-6-2014 - velocity is zero
f_max = 0 #fraction in maxwellian component
kT_max = 0 #energy of maxwellian component
nic = 0 #number of background photon field
ictemp = 0 #temperature of background photon field
icnorm = 0 #normalization of background photon field
tstep = -1
#===========================================
runner = Output()
runner.gen_output(tstep,esn_,mej_,nism_,brakind_,tau_,age_,e0_,velpsr,etag_,
		etab_,emin_,emax_,ebreak_,p1_,p2_,f_max,kT_max,nic,ictemp,icnorm,
		dynstep=False,elecstep=False,photstep=False,directory_path=directory_test,speedup=True)

default_model = [0.23137317916206487, 0.16677256034615273, 0.11788157521875939, 0.06733072391456521, 
			8.6986931406718533, 1.9777813143963134, 0.090578178617320884, 3.4109988771503787, 
			1.9405766133480606, 104.56363487663938]

os.chdir(directory_test)
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

print(model)
def calc_chi_sqr(model_calc):
	total = 0
	for data, model in zip(model_calc,default_model):
		total += (float(model)-float(data))**2
	reduced_total = total/len(model_calc)
	return total, reduced_total
chisqur, reduced_chisqur = calc_chi_sqr(model)
print(chisqur, reduced_chisqur)

# time, radius = reader.radius_info()
# time = list(time)
# radius = list(radius)

# grapher = Graphs(title="Radius vs. Time",xlabel="Log Time (yr)",ylabel="Radius (parsec)")
# fig, ax = grapher.create_figure_logxory(x_data=time,y_data=[radius],xlog=True)
# plt.show()
