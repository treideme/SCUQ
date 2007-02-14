# You have to import this module to use si units.
from scuq import *

# Lets at first demonstrate what happens if a unit
# symbol is used twice.

try:
    myNewton = units.AlternateUnit("N", 
                        si.KILOGRAM*si.METER/si.SECOND**2)
except qexceptions.UnitExistsException, exp:
    # "The following base unit has already been defined : N"
    # ... you should not create units having the same 
		# symbol twice.
    print str(exp)
    
# Define the unit dynamic
myNewton = units.AlternateUnit("MN", 
                          si.KILOGRAM*si.METER/si.SECOND**2)

# "MN"
print str(myNewton)

# "False", since they have different symbols
print "myNewton == si.NEWTON: "+str(myNewton == si.NEWTON)

# However they describe the same physical dimension, thus...
print "myNewton.is_compatible(si.NEWTON): "\
       +str(myNewton.is_compatible(si.NEWTON))
