# You have to import this module to use SI units.
from scuq import *

# Transformed units can be defined in the same physical dimension 
# as a base unit by using the transformations below.

# 1. Adding an offset to a unit (i.e. degrees Celsius based on 
#    Kelvin)
celsius        = si.KELVIN + 273.15
# 2. Dividing it by a constant value (i.e. dyn based on Newton)
dyn            = si.NEWTON / 100000
# 3. Muliplying it by an absolute constant value (i.e. 
#    pound force from Newton)
lbf            = si.NEWTON * 4.4482216152605

# These transformations allow conversion among the
# units that describe the same physical dimension.

# This converts the unit back to the system unit, which is
# Kelvins in this case.
operator = celsius.to_system_unit()
result = operator.convert(1)
assert(result == -272.15)

# the same again for dyn -> Newton...
operator = dyn.to_system_unit()
result = operator.convert(1)
assert(result - 1e5 < 1e-10)

# the same again for lbf -> Newton...
operator = lbf.to_system_unit()
result = operator.convert(1)
assert(result - 0.2248089431 < 1e-10)

# You can also get an operator to convert among the
# transformed units: dyn -> lbf
operator = dyn.get_operator_to(lbf)
result   = operator.convert(1)
assert(result - 444822 < 0.5)
