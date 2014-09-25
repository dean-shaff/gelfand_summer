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
class Output(object):
	def __init__(self):
		pass
	def gen_output(self,tstep,esn,mej,
			nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,
			nic,ictemp,icnorm,dynstep=False,elecstep=False,photstep=False,
			directory_path=False,speedup=False):
		"""
		dynstep, elecstep, photstep specify whether or not to use those parameters in the model run
		directory_path indicates where to move the .fits files created by the model. If nothing is specified, it moves to the default_fits folder in the mcmc folder.
		speedup specifies whether or not to use MY modifications to gelfand's code or not. 
		"""
		t = float(time.time()) 
		filename = str(datetime.datetime.today())
		if speedup == False:
			os.chdir(path_to_pwn)
			if dynstep==False and elecstep==False and photstep==False:
				if tstep != -1:
					call = './pwnmodel.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(tstep,esn,mej,
						nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic)
				elif tstep == -1:
					call = './pwnmodel.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(tstep,esn,mej,
						nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic,ictemp,icnorm)
			else:
				call = './pwnmodel.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} [{} {} {}]'.format(tstep,esn,mej,
					nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic, ictemp, icnorm, dynstep, elecstep, photstep)
			subprocess.call(call,shell=True)
		elif speedup == True:
			os.chdir(path_to_speed)
			if dynstep==False and elecstep==False and photstep==False:
				if tstep != -1:
					call = './pwnmodeldeanmod.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(tstep,esn,mej,
						nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic)
				elif tstep == -1:
					call = './pwnmodeldeanmod.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(tstep,esn,mej,
						nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic,ictemp,icnorm)
			else:
				call = './pwnmodeldeanmod.exe {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} [{} {} {}]'.format(tstep,esn,mej,
					nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic, ictemp, icnorm, dynstep, elecstep, photstep)
			subprocess.call(call,shell=True)
		print("time in calculation: {}".format(float(time.time()) - t))
		if directory_path == False:
			subprocess.call('mv *.fits {}'.format(path_default),shell = True)
			os.chdir(path_default) 
		elif directory_path != False:
			subprocess.call('mv *.fits {}'.format(directory_path),shell = True)
			os.chdir(directory_path) 
		

	def delete_fits(self):
		os.chdir(mcmc_path)
		subprocess.call('rm *.fits',shell=True)
