# ATTENTION: You must NOT encapsulate quantities in uncertain 
# components.
# this violates our design. Instead use the followin approach...

# You have to import this module to use quantities and uncertain 
# values.
from scuq import *
# You have to import this module to use NumPy
import numpy as n

# You have to define the uncertain value first.
# This creates an uncertain value 1.0+-0.2
uvalue = ucomponents.UncertainInput(1.0, 0.2)

# Now you may encapsulate it in a quantity
# This creates a quantity (1.0+-0.2) [m]
uquantitiy = quantities.Quantity(si.METER, uvalue)

# Now you may build a model
# This creates a quantitiy that has m^(1/2) as unit and
# the propagation of the uncertainty is also performed.
model_1 = n.sqrt(uquantitiy)
assert(model_1.get_default_unit() == n.sqrt(si.METER))

# Create a context for the uncertainty evaluation.
c = ucomponents.Context()

# Evaluate the input VALUE
u_c = c.uncertainty(uvalue)                      
assert(u_c == 0.2)          # ...as expected

# Evaluate the input QUANTITY
u_c = c.uncertainty(uquantitiy)
# this one has a unit (!)
assert(u_c == quantities.Quantity(si.METER,0.2)) 

# Evaluate the model
u_c = c.uncertainty(model_1)                     
# ... the correct unit.
assert(u_c == 
  quantities.Quantity(n.sqrt(si.METER),0.1))
