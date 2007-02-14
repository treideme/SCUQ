from scuq import *
from numpy import *

c = cucomponents.Context()

# Define complex j
_J_ = quantities.Quantity(units.ONE, c.gaussian(0+1j, 0, 0))

tmp = c.gaussian(4.9990, 0.003209, 0.0)
v   = quantities.Quantity(si.VOLT, tmp)
tmp = c.gaussian(19.661e-3, 0.00947e-3, 0.0)
i   = quantities.Quantity(si.AMPERE, tmp)
tmp = c.gaussian(1.04446, 0.0007521, 0.0)
phi = quantities.Quantity(si.RADIAN, tmp)

# Define the model
Z   = v / i * exp( _J_ * phi )

# Verify model
assert(Z.get_default_unit().is_compatible(si.OHM))

# Correlate input quantities
c.set_correlation(v,i,matrix([[-0.36, 0], [0, 0]])) 
c.set_correlation(v,phi,matrix([[+0.86, 0], [0, 0]]))
c.set_correlation(i,phi,matrix([[ -0.65, 0], [0, 0]]))

# Report the uncertainty
u_c = c.uncertainty(Z)
print "u(Z) =\n", c.uncertainty(Z)
# evaluate u(Re) and u(Im) explicitly

unit = u_c.get_default_unit()
val = u_c.get_value(unit)
u_r = quantities.Quantity(sqrt(unit),sqrt(val[0,0]))
u_i = quantities.Quantity(sqrt(unit),sqrt(val[1,1]))

print "u(R) = ",u_r
print "u(I) = ",u_i


assert(u_c.get_default_unit().is_compatible(si.OHM**2))
