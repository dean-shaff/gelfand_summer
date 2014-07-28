
import matplotlib as mpl
#mpl.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm 
import numpy as np
from matplotlib import rc 
#print(fm.findSystemFonts())

# path = '/home/dean/Documents/times.tff'
# filename = 'times.tff'
# prop = fm.FontProperties(fname=path)

#print(mpl.matplotlib_fname())
#print(mpl.get_configdir())

#mpl.rcParams['font.family'] = 'serif'
rc('font',family='serif',serif='Ubuntu')
x = np.arange(0,10,0.1)
y = np.sin(x)

plt.plot(x,y,'k')
plt.title("Sine!",fontsize=24)
plt.show()