from numpy import *
from scuq import *

# generate some data, of a measured quantity
data = array([quantities.Quantity(si.VOLT, cos(50 * t)) \
              for t in xrange(1000)])

# the problem is, NumPy doesn't accept object
# arguments for the fft module; therefore,
# the data must be converted to the numpy
# float type.

# Enable weak consistency checking to convert to float64,
# the python floating point type.
quantities.set_strict(False)
f_data = float64(data)
quantities.set_strict(True)

# perform fft
ff_data = fft.fft(f_data)

# the result will also be the numpy complex type
assert(ff_data.dtype == complex)
