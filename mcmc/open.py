import os
import subprocess

path1 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing1'
path2 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing2'
path3 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing3'
path4 = '/home/dean/python_stuff_ubuntu/gelfand_summer/mcmc/testing4'
filename = 'log1wedaugust.txt'

os.chdir(path1)
subprocess.call('subl {}'.format(filename),shell=True)
os.chdir(path2)
subprocess.call('subl {}'.format(filename),shell=True)
os.chdir(path3)
subprocess.call('subl {}'.format(filename),shell=True)
os.chdir(path4)
subprocess.call('subl {}'.format(filename),shell=True)
