from scuq import *
from numpy import *

c = ucomponents.Context()

tmp = ucomponents.UncertainInput.gaussian(4.9990, 0.0032)
v   = quantities.Quantity(si.VOLT, tmp)
tmp = ucomponents.UncertainInput.gaussian(19.661e-3, 0.0095e-3)
i   = quantities.Quantity(si.AMPERE, tmp)
tmp = ucomponents.UncertainInput.gaussian(1.04446, 0.00075)
phi = quantities.Quantity(si.RADIAN, tmp)

# Define the model
R   = v / i * cos(phi)
X   = v / i * sin(phi)
Z   = v / i

# Verify model
assert(R.get_default_unit().is_compatible(si.OHM))
assert(X.get_default_unit().is_compatible(si.OHM))
assert(Z.get_default_unit().is_compatible(si.OHM))

c.set_correlation(v,i,-0.36) 
c.set_correlation(v,phi, +0.86)
c.set_correlation(i,phi, -0.65)

print "u(R) = ", c.uncertainty(R)
print "u(X) = ", c.uncertainty(X)
print "u(Z) = ", c.uncertainty(Z)
