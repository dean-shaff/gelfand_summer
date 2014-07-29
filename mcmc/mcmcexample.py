import numpy as np 
import scipy.optimize as op

jump = 1
# Choose the "true" parameters.
m_true = -0.9594
b_true = 4.294
f_true = 0.534

#initial guess for optimization:
m_guess = -1
b_guess = 4.5
f_guess = 0.5
# Generate some synthetic data from the model.
N = 50
x = np.sort(10*np.random.rand(N))
yerr = 0.1+0.5*np.random.rand(N)
y = m_true*x+b_true
y += np.abs(f_true*y) * np.random.randn(N)
y += yerr * np.random.randn(N)

def lnlike(theta, x, y, yerr):
    m, b, lnf = theta
    model = m * x + b
    inv_sigma2 = 1.0/(yerr**2 + model**2*np.exp(2*lnf))
    return -0.5*(np.sum((y-model)**2*inv_sigma2 - np.log(inv_sigma2)))

def callbackF(theta):
	m, b, lnf = theta
	global jump
	print("{} {} {} {}".format(jump,m, b, lnf))
	jump += 1

def optimize():
	nll = lambda *args: -lnlike(*args)
	result = op.minimize(nll, [m_guess, b_guess, np.log(f_guess)], args=(x, y, yerr),method="Nelder-Mead",options={'disp':True,'maxfev':300},callback=callbackF)
	m_ml, b_ml, lnf_ml = result["x"]
	print(result["success"])
	return  result["x"]#, [m_ml, b_ml, lnf_ml] # list([m_ml, b_ml, lnf_ml])
print(optimize())