from scuq import *

# Define the units as transformed units
NANOMETER = si.METER/1e9
CELSIUS   = si.KELVIN+273.15
print "nm := ",NANOMETER
print "C  := ",CELSIUS

c = ucomponents.Context()

tmp = ucomponents.UncertainComponent.gaussian(5e7, 25, 18)
l_s = quantities.Quantity(NANOMETER, tmp)

tmp = ucomponents.UncertainComponent.gaussian(0.0, 5.8, 24)
d_1 = quantities.Quantity(NANOMETER, tmp)
tmp = ucomponents.UncertainComponent.gaussian(0.0, 3.9, 5)
d_2 = quantities.Quantity(NANOMETER, tmp)
tmp = ucomponents.UncertainComponent.gaussian(0.0, 6.7, 8)
d_3 = quantities.Quantity(NANOMETER, tmp)

d = d_1 + d_2 + d_3

# Verify the model
assert(d.get_default_unit() == NANOMETER)

tmp = ucomponents.UncertainComponent.uniform(11.5e-6, 2e-6)
alpha_s     = quantities.Quantity(~CELSIUS, tmp)
tmp = ucomponents.UncertainComponent.uniform(0.0, 1e-6, 50)
delta_alpha = quantities.Quantity(~CELSIUS, tmp)

tmp = ucomponents.UncertainComponent.gaussian(-0.1, 0.2)
theta_1 = quantities.Quantity(CELSIUS, tmp)
tmp = ucomponents.UncertainComponent.arcsine(0.0)
theta_2 = quantities.Quantity(CELSIUS, tmp)
theta = theta_1 + theta_2

# Verify the model
assert(theta.get_default_unit() == CELSIUS)

tmp = ucomponents.UncertainComponent.uniform(0.0, 0.05, 2)
delta_theta = quantities.Quantity(CELSIUS, tmp)

tmp_1 = -l_s * delta_alpha * theta
tmp_2 = l_s * alpha_s * delta_theta

l = l_s + d + tmp_1 + tmp_2

# Verify the model
assert(l.get_default_unit() == NANOMETER)

print "u(alpha_s)\t\t\t= ",c.uncertainty(alpha_s)
print "u(delta_alpha)\t\t\t= ",c.uncertainty(delta_alpha)
print "u(theta)\t\t\t= ",c.uncertainty(theta)
print "u(-l_s * delta_alpha * theta)\t= ", \
	c.uncertainty(tmp_1)
print "u(l_s * alpha_s * delta_theta)\t= ", \
	c.uncertainty(tmp_2)
quantities.set_strict(False) # Enable conversion of units
print "u(l)\t\t\t\t= ", \
	c.uncertainty(l).get_value(si.METER),si.METER
print "dof(l)\t\t\t\t= ",c.dof(l)
