from scuq import *
from numpy import *

# generate some quantity
q = quantities.Quantity(si.VOLT, 10)	

# generate a matrix
m = matrix([[q, q], [q, -q]])

# enable weak consistency checks for conversion
quantities.set_strict(False)

# invert the matrix (converts to float automatically)
result = linalg.inv(m)

quantities.set_strict(True)
 
assert(result.dtype == float)
