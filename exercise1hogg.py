import numpy as np 
import numpy.linalg as linalg
import matplotlib.pyplot as plt

from plotting_tools import Graphs

blah = """
5 203 495 21 5 -0.33
6 58 173 15 9 0.67
7 210 479 27 4 -0.02
8 202 504 14 4 -0.05
9 198 510 30 11 -0.84
10 158 416 16 7 -0.69
11 165 393 14 5 0.30
12 201 442 25 5 -0.46
13 157 317 52 5 -0.03
14 131 311 16 6 0.50
15 166 400 34 6 0.73
16 160 337 31 5 -0.52
17 186 423 42 9 0.90
18 125 334 26 8 0.40
19 218 533 16 6 -0.78
20 146 344 22 5 -0.56
"""

blah = list(blah.split(" "))
x = np.array([float(blah[(i*5)+1]) for i in xrange(0,int(len(blah))/5)])
y = [float(blah[(i*5)+2]) for i in xrange(0,int(len(blah))/5)]
sigma_y = [float(blah[(i*5)+3]) for i in xrange(0,int(len(blah))/5)]

A_trans = np.array([np.ones(len(x)),x,x**2,x**3])
C = np.diag(sigma_y)
sol = np.dot(linalg.inv(np.dot(A_trans,np.dot(linalg.inv(C),np.transpose(A_trans)))),np.dot(A_trans,np.dot(linalg.inv(C),y)))
dummy = Graphs()
fig, ax = dummy.basic_plot()
plt.plot(np.arange(0,300,1),sol[0]+(sol[1]*np.arange(0,300,1))+(sol[2]*np.arange(0,300,1)**2)+(sol[3]*np.arange(0,300,1)**3),'k',linewidth=2)
ax.errorbar(x,y,yerr=sigma_y,fmt='.',color='k',ecolor='k')
fig.show()
raw_input(">> ")
