#program that runs pwn model
import os
import subprocess
import time
import datetime
#Parameters=====================
tstep = 100 #time step (only takes integer values) 21-6-2014 changed tstep from 1000 to 100
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
	t = float(time.time()) #just so I can get the timing... I want to start a big csv file that has ALL my runtimes...
	date = str(datetime.date.today())
	os.chdir(path_to_pwn)
	subprocess.call('./pwnmodel.exe %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r' %(tstep,esn,mej,
		nism,brakind,tau,age,e0,velpsr,etag,etab,emin,emax,ebreak,p1,p2,f_max,kT_max,nic),shell=True)
	subprocess.call('mkdir %s' %date,shell=True)
	subprocess.call('mv *.fits %s/%s' % (path_to_pwn,date),shell = True) 
	print float(time.time()) - time 
main()